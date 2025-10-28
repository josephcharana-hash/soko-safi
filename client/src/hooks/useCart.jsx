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
    setCartCount(cartItems.reduce((sum, item) => sum + item.quantity, 0))
  }, [cartItems])

  const loadCart = async () => {
    try {
      setLoading(true)
      const cart = await api.cart.get()
      setCartItems(cart || [])
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
      await loadCart() // Refresh cart
      return true
    } catch (error) {
      console.error('Failed to add to cart:', error)
      throw error
    }
  }

  const updateQuantity = async (itemId, quantity) => {
    try {
      await api.cart.update(itemId, quantity)
      setCartItems(cartItems.map(item => 
        item.id === itemId ? { ...item, quantity } : item
      ))
      return true
    } catch (error) {
      console.error('Failed to update quantity:', error)
      throw error
    }
  }

  const removeFromCart = async (itemId) => {
    try {
      await api.cart.remove(itemId)
      setCartItems(cartItems.filter(item => item.id !== itemId))
      return true
    } catch (error) {
      console.error('Failed to remove from cart:', error)
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