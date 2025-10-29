import { useState, useEffect, createContext, useContext } from 'react'
import { api } from '../services/api'

const CartContext = createContext()

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [cartCount, setCartCount] = useState(0)

  useEffect(() => {
    loadCart()
  }, [])

  useEffect(() => {
    if (Array.isArray(cartItems)) {
      setCartCount(cartItems.reduce((sum, item) => sum + item.quantity, 0))
    } else {
      setCartCount(0)
    }
  }, [cartItems])

  const loadCart = async () => {
    try {
      setLoading(true)
      const cart = await api.cart.get()
      console.log('Loading cart, received:', cart)
      
      // Handle different response formats from backend
      if (Array.isArray(cart)) {
        setCartItems(cart)
      } else if (cart && Array.isArray(cart.items)) {
        setCartItems(cart.items)
      } else if (cart && Array.isArray(cart.cart_items)) {
        setCartItems(cart.cart_items)
      } else if (cart && cart.data && Array.isArray(cart.data)) {
        setCartItems(cart.data)
      } else {
        console.log('Cart format not recognized, setting empty:', cart)
        setCartItems([])
      }
    } catch (error) {
      console.error('Failed to load cart:', error)
      setCartItems([])
    } finally {
      setLoading(false)
    }
  }

  const addToCart = async (productId, quantity = 1) => {
    try {
      await api.cart.add(productId, quantity)
      await loadCart() // Reload the cart from the server
      return true
    } catch (error) {
      console.error('Failed to add to cart:', error)
      // even if it fails, we can try to load the cart to sync
      await loadCart()
      return false // return false because the add operation failed
    }
  }

  const updateQuantity = async (itemId, quantity) => {
    try {
      await api.cart.update(itemId, quantity)
      // Optimistically update UI
      setCartItems(prev => prev.map(item => 
        item.id === itemId ? { ...item, quantity } : item
      ))
      return true
    } catch (error) {
      console.error('Failed to update quantity:', error)
      // Reload cart on error to sync with server
      await loadCart()
      throw error
    }
  }

  const removeFromCart = async (itemId) => {
    try {
      await api.cart.remove(itemId)
      // Optimistically update UI
      setCartItems(prev => prev.filter(item => item.id !== itemId))
      return true
    } catch (error) {
      console.error('Failed to remove from cart:', error)
      // Reload cart on error to sync with server
      await loadCart()
      throw error
    }
  }

  const clearCart = async () => {
    try {
      await api.cart.clear()
      setCartItems([])
      return true
    } catch (error) {
      console.error('Failed to clear cart:', error)
      throw error
    }
  }

  const getCartTotal = () => {
    if (!Array.isArray(cartItems)) return 0
    return cartItems.reduce((sum, item) => {
      const price = typeof item.price === 'string' ? parseFloat(item.price) : item.price
      return sum + (price * item.quantity)
    }, 0)
  }

  const value = {
    cartItems,
    loading,
    cartCount,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    loadCart,
    getCartTotal
  }

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  )
}

export const useCart = () => {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}