import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Diamond, Trash2, Plus, Minus, ShoppingBag } from "lucide-react";
import Navbar from "../Components/Layout/Navbar";
import Footer from "../Components/Layout/Footer";

const CartPage = () => {
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useState([
    {
      id: 1,
      productId: 1,
      title: "Ceramic Vase",
      artisan: "Sarah Johnson",
      price: 45.0,
      quantity: 1,
      image:
        "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=100&h=100&fit=crop",
    },
    {
      id: 2,
      productId: 2,
      title: "Wood Carving",
      artisan: "John Smith",
      price: 120.0,
      quantity: 2,
      image:
        "https://images.unsplash.com/photo-1551522435-a13afa10f103?w=100&h=100&fit=crop",
    },
    {
      id: 3,
      productId: 3,
      title: "Textile Art",
      artisan: "Maria Garcia",
      price: 85.0,
      quantity: 1,
      image:
        "https://images.unsplash.com/photo-1558769132-cb1aea3c8565?w=100&h=100&fit=crop",
    },
  ]);

  const updateQuantity = (id, newQuantity) => {
    if (newQuantity < 1) return;
    setCartItems(
      cartItems.map((item) =>
        item.id === id ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  const removeItem = (id) => {
    setCartItems(cartItems.filter((item) => item.id !== id));
  };

  const subtotal = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const shipping = 10.0;
  const tax = subtotal * 0.1;
  const total = subtotal + shipping + tax;

  const handleCheckout = () => {
    navigate("/checkout");
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />

      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">
            Shopping Cart
          </h1>

          {cartItems.length === 0 ? (
            <div className="bg-white rounded-2xl shadow-sm p-12 text-center">
              <ShoppingBag className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Your cart is empty
              </h2>
              <p className="text-gray-600 mb-6">
                Add some beautiful handcrafted items to get started!
              </p>
              <Link
                to="/explore"
                className="btn-primary inline-block px-6 py-3"
              >
                Explore Products
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Cart Items */}
              <div className="lg:col-span-2 space-y-4">
                {cartItems.map((item) => (
                  <div
                    key={item.id}
                    className="bg-white rounded-xl shadow-sm p-6"
                  >
                    <div className="flex items-start space-x-4">
                      <Link to={`/product/${item.productId}`}>
                        <img
                          src={item.image}
                          alt={item.title}
                          className="w-24 h-24 rounded-lg object-cover"
                        />
                      </Link>
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <Link
                              to={`/product/${item.productId}`}
                              className="text-lg font-bold text-gray-900 hover:text-primary"
                            >
                              {item.title}
                            </Link>
                            <p className="text-sm text-gray-600">
                              by {item.artisan}
                            </p>
                          </div>
                          <button
                            onClick={() => removeItem(item.id)}
                            className="p-2 text-gray-400 hover:text-red-500 transition-colors"
                          >
                            <Trash2 className="w-5 h-5" />
                          </button>
                        </div>

                        <div className="flex items-center justify-between mt-4">
                          <div className="flex items-center space-x-3">
                            <button
                              onClick={() =>
                                updateQuantity(item.id, item.quantity - 1)
                              }
                              className="w-8 h-8 rounded-lg border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                            >
                              <Minus className="w-4 h-4" />
                            </button>
                            <span className="text-lg font-medium w-8 text-center">
                              {item.quantity}
                            </span>
                            <button
                              onClick={() =>
                                updateQuantity(item.id, item.quantity + 1)
                              }
                              className="w-8 h-8 rounded-lg border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                            >
                              <Plus className="w-4 h-4" />
                            </button>
                          </div>
                          <p className="text-xl font-bold text-gray-900">
                            ${(item.price * item.quantity).toFixed(2)}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Order Summary */}
              <div className="lg:col-span-1">
                <div className="bg-white rounded-xl shadow-sm p-6 sticky top-8">
                  <h2 className="text-xl font-bold text-gray-900 mb-6">
                    Order Summary
                  </h2>

                  <div className="space-y-3 mb-6">
                    <div className="flex items-center justify-between text-gray-700">
                      <span>Subtotal ({cartItems.length} items)</span>
                      <span className="font-medium">
                        ${subtotal.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-gray-700">
                      <span>Shipping</span>
                      <span className="font-medium">
                        ${shipping.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-gray-700">
                      <span>Tax</span>
                      <span className="font-medium">${tax.toFixed(2)}</span>
                    </div>
                    <div className="border-t border-gray-200 pt-3 mt-3">
                      <div className="flex items-center justify-between">
                        <span className="text-lg font-bold text-gray-900">
                          Total
                        </span>
                        <span className="text-2xl font-bold text-gray-900">
                          ${total.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={handleCheckout}
                    className="w-full btn-primary py-3 text-lg mb-4"
                  >
                    Proceed to Checkout
                  </button>

                  <Link
                    to="/explore"
                    className="block text-center text-primary hover:text-primary-hover font-medium"
                  >
                    Continue Shopping
                  </Link>

                  {/* Trust Badges */}
                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <p className="text-sm text-gray-600 mb-3">We accept:</p>
                    <div className="flex items-center space-x-3">
                      <div className="px-3 py-2 bg-gray-100 rounded text-xs font-medium text-gray-700">
                        Visa
                      </div>
                      <div className="px-3 py-2 bg-gray-100 rounded text-xs font-medium text-gray-700">
                        Mastercard
                      </div>
                      <div className="px-3 py-2 bg-gray-100 rounded text-xs font-medium text-gray-700">
                        PayPal
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default CartPage;
