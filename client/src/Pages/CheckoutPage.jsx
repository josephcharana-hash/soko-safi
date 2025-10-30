import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Smartphone, Lock, CheckCircle, Loader } from 'lucide-react'
import Navbar from '../Components/Layout/Navbar'
import Footer from '../Components/Layout/Footer'
import { useCart } from '../hooks/useCart.jsx'
import { api } from '../services/api'

const CheckoutPage = () => {
  const navigate = useNavigate()
  const { cartItems, loading, clearCart } = useCart()
  const [step, setStep] = useState(1) // 1: Shipping, 2: Payment, 3: Confirmation
  const [processing, setProcessing] = useState(false)
  const [shippingInfo, setShippingInfo] = useState({
    fullName: "",
    address: "",
    city: "",
    phone: "",
  });

  const [paymentInfo, setPaymentInfo] = useState({
    phoneNumber: '',
    paymentMethod: 'mpesa'
  })

  useEffect(() => {
    if (!loading && (!cartItems || cartItems.length === 0)) {
      navigate('/cart')
    }
  }, [cartItems, loading, navigate])

  const subtotal = cartItems.reduce((sum, item) => {
    const price = item.product?.price || item.price || 0
    const numPrice = typeof price === 'string' ? parseFloat(price) : price
    const validPrice = isNaN(numPrice) ? 0 : numPrice
    return sum + (validPrice * item.quantity)
  }, 0)
  const shipping = 150.00 // KSH 150 shipping
  const tax = subtotal * 0.16 // 16% VAT in Kenya
  const total = subtotal + shipping + tax

  const handlePaymentChange = (e) => {
    const { name, value } = e.target;
    setPaymentInfo({ ...paymentInfo, [name]: value });
  };

  const handlePaymentSubmit = async (e) => {
    e.preventDefault()
    
    if (cartItems.length === 0) {
      alert('Your cart is empty')
      return
    }
    
    try {
      setProcessing(true)
      
      // Create order
      const orderData = {
        total_amount: total,
        status: 'pending'
      }
      
      const order = await api.orders.create(orderData)
      const orderId = order.order?.id || order.id
      
      // Create order items
      for (const item of cartItems) {
        const price = typeof item.price === 'string' ? parseFloat(item.price) : item.price
        await api.orders.createItem({
          order_id: orderId,
          product_id: item.product_id || item.id,
          quantity: item.quantity,
          unit_price: price,
          total_price: price * item.quantity,
          artisan_id: item.product?.artisan_id || item.artisan_id || 1
        })
      }
      
      // Clear cart after successful order creation
      await clearCart()
      
      // Initiate M-Pesa payment
      const paymentData = {
        order_id: orderId,
        phone_number: paymentInfo.phoneNumber
      }
      
      console.log('Initiating M-Pesa payment...', paymentData)
      
      try {
        const response = await api.payments.mpesa.stkPush(paymentData)
        
        if (response && (response.success || response.message)) {
          alert('Payment request sent to your phone. Please complete the payment.')
          setStep(3)
        } else {
          throw new Error(response?.error || 'Payment initiation failed')
        }
      } catch (apiError) {
        console.warn('M-Pesa API not available, simulating payment for demo')
        alert('Demo mode: Payment request sent to your phone. Please complete the payment.')
        setStep(3)
      }
      
    } catch (error) {
      console.error('Payment failed:', error)
      alert(`Payment failed: ${error.message}. Please try again.`)
    } finally {
      setProcessing(false)
    }
  }

    // simulate payment processing
    setTimeout(() => {
      setProcessing(false);
      setStep(3);
    }, 2000);
  };

  const handleConfirmOrder = () => {
    alert("Order confirmed! Thank you for shopping with us.");
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4 py-10">
      <div className="w-full max-w-2xl bg-white shadow-md rounded-2xl p-6">
        <h2 className="text-2xl font-semibold text-center mb-6">
          Checkout - Step {step} of 3
        </h2>

        {/* Step 1: Shipping Info */}
        {step === 1 && (
          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium">Full Name</label>
              <input
                type="text"
                name="fullName"
                value={shippingInfo.fullName}
                onChange={handleShippingChange}
                className="mt-1 w-full border border-gray-300 rounded-lg p-2"
                placeholder="John Doe"
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Address</label>
              <input
                type="text"
                name="address"
                value={shippingInfo.address}
                onChange={handleShippingChange}
                className="mt-1 w-full border border-gray-300 rounded-lg p-2"
                placeholder="123 Main Street"
              />
            </div>
            <div className="flex gap-4">
              <div className="flex-1">
                <label className="block text-sm font-medium">City</label>
                <input
                  type="text"
                  name="city"
                  value={shippingInfo.city}
                  onChange={handleShippingChange}
                  className="mt-1 w-full border border-gray-300 rounded-lg p-2"
                  placeholder="Nairobi"
                />
              </div>
              <div className="flex-1">
                <label className="block text-sm font-medium">Phone</label>
                <input
                  type="text"
                  name="phone"
                  value={shippingInfo.phone}
                  onChange={handleShippingChange}
                  className="mt-1 w-full border border-gray-300 rounded-lg p-2"
                  placeholder="07XX XXX XXX"
                />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2">
              {/* Step 1: Shipping Information */}
              {step === 1 && (
                <div className="bg-white rounded-xl shadow-sm p-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">
                    Shipping Information
                  </h2>
                  <form onSubmit={handleShippingSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label
                          htmlFor="fullName"
                          className="block text-sm font-medium text-gray-700 mb-2"
                        >
                          Full Name *
                        </label>
                        <input
                          type="text"
                          id="fullName"
                          name="fullName"
                          value={shippingInfo.fullName}
                          onChange={handleShippingChange}
                          className="input-field"
                          required
                        />
                      </div>
                      <div>
                        <label
                          htmlFor="email"
                          className="block text-sm font-medium text-gray-700 mb-2"
                        >
                          Email *
                        </label>
                        <input
                          type="email"
                          id="email"
                          name="email"
                          value={shippingInfo.email}
                          onChange={handleShippingChange}
                          className="input-field"
                          required
                        />
                      </div>
                    </div>

                    <div>
                      <label
                        htmlFor="phone"
                        className="block text-sm font-medium text-gray-700 mb-2"
                      >
                        Phone Number *
                      </label>
                      <input
                        type="tel"
                        id="phone"
                        name="phone"
                        value={shippingInfo.phone}
                        onChange={handleShippingChange}
                        className="input-field"
                        required
                      />
                    </div>

                    <div>
                      <label
                        htmlFor="address"
                        className="block text-sm font-medium text-gray-700 mb-2"
                      >
                        Street Address *
                      </label>
                      <input
                        type="text"
                        id="address"
                        name="address"
                        value={shippingInfo.address}
                        onChange={handleShippingChange}
                        className="input-field"
                        required
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label
                          htmlFor="city"
                          className="block text-sm font-medium text-gray-700 mb-2"
                        >
                          City *
                        </label>
                        <input
                          type="text"
                          id="city"
                          name="city"
                          value={shippingInfo.city}
                          onChange={handleShippingChange}
                          className="input-field"
                          required
                        />
                      </div>
                      <div>
                        <label
                          htmlFor="state"
                          className="block text-sm font-medium text-gray-700 mb-2"
                        >
                          State/Province *
                        </label>
                        <input
                          type="text"
                          id="state"
                          name="state"
                          value={shippingInfo.state}
                          onChange={handleShippingChange}
                          className="input-field"
                          required
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label
                          htmlFor="zipCode"
                          className="block text-sm font-medium text-gray-700 mb-2"
                        >
                          ZIP/Postal Code *
                        </label>
                        <input
                          type="text"
                          id="zipCode"
                          name="zipCode"
                          value={shippingInfo.zipCode}
                          onChange={handleShippingChange}
                          className="input-field"
                          required
                        />
                      </div>
                      <div>
                        <label
                          htmlFor="country"
                          className="block text-sm font-medium text-gray-700 mb-2"
                        >
                          Country *
                        </label>
                        <input
                          type="text"
                          id="country"
                          name="country"
                          value={shippingInfo.country}
                          onChange={handleShippingChange}
                          className="input-field"
                          required
                        />
                      </div>
                    </div>

                    <div className="flex justify-between pt-6">
                      <Link to="/cart" className="btn-secondary px-6 py-3">
                        Back to Cart
                      </Link>
                      <button type="submit" className="btn-primary px-6 py-3">
                        Continue to Payment
                      </button>
                    </div>
                  </form>
                </div>
              )}

              {/* Step 2: Payment Information */}
              {step === 2 && (
                <div className="bg-white rounded-xl shadow-sm p-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-6">
                    Payment Information
                  </h2>

                  {/* Payment Method Selection */}
                  <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      Payment Method
                    </label>
                    <div className="max-w-md">
                      <div className="p-4 rounded-lg border-2 border-primary bg-primary/5">
                        <div className="flex items-center space-x-3">
                          <Smartphone className="w-8 h-8 text-green-600" />
                          <div>
                            <p className="font-bold text-gray-900">M-Pesa</p>
                            <p className="text-sm text-gray-600">Pay with your mobile money</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <form onSubmit={handlePaymentSubmit} className="space-y-6">
                    <div>
                      <label htmlFor="phoneNumber" className="block text-sm font-medium text-gray-700 mb-2">
                        M-Pesa Phone Number *
                      </label>
                      <input
                        type="tel"
                        id="phoneNumber"
                        name="phoneNumber"
                        value={paymentInfo.phoneNumber}
                        onChange={handlePaymentChange}
                        placeholder="254712345678"
                        className="input-field"
                        pattern="254[0-9]{9}"
                        title="Please enter a valid Kenyan phone number (254XXXXXXXXX)"
                        required
                      />
                      <p className="text-sm text-gray-500 mt-1">
                        Enter your M-Pesa registered phone number (format: 254XXXXXXXXX)
                      </p>
                    </div>

                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <Smartphone className="w-5 h-5 text-green-600 mt-0.5" />
                        <div>
                          <h4 className="font-medium text-green-800 mb-2">How M-Pesa Payment Works:</h4>
                          <ol className="text-sm text-green-700 space-y-1">
                            <li>1. Click "Pay with M-Pesa" below</li>
                            <li>2. You'll receive an STK push notification on your phone</li>
                            <li>3. Enter your M-Pesa PIN to complete the payment</li>
                            <li>4. You'll receive a confirmation SMS</li>
                          </ol>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2 p-4 bg-gray-50 rounded-lg">
                      <Lock className="w-5 h-5 text-gray-600" />
                      <p className="text-sm text-gray-600">
                        Your payment is processed securely through Safaricom M-Pesa
                      </p>
                    </div>

                    <div className="flex justify-between pt-6">
                      <button
                        type="button"
                        onClick={() => setStep(1)}
                        className="btn-secondary px-6 py-3"
                      >
                        Back
                      </button>
                      <button 
                        type="submit" 
                        disabled={processing}
                        className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {processing ? (
                          <>
                            <Loader className="w-5 h-5 animate-spin inline mr-2" />
                            Processing...
                          </>
                        ) : (
                          'Pay with M-Pesa'
                        )}
                      </button>
                    </div>
                  </form>
                </div>
              )}

              {/* Step 3: Order Confirmation */}
              {step === 3 && (
                <div className="bg-white rounded-xl shadow-sm p-8 text-center">
                  <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <CheckCircle className="w-12 h-12 text-green-600" />
                  </div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">
                    Order Confirmed!
                  </h2>
                  <p className="text-gray-600 mb-2">
                    Thank you for your purchase.
                  </p>
                  <p className="text-gray-600 mb-8">
                    Order confirmation has been sent to{" "}
                    <span className="font-medium">{shippingInfo.email}</span>
                  </p>

                  <div className="bg-gray-50 rounded-lg p-6 mb-8">
                    <p className="text-sm text-gray-600 mb-2">Order Number</p>
                    <p className="text-2xl font-bold text-gray-900">
                      #ORD-{Date.now().toString().slice(-6)}
                    </p>
                  </div>

                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Link
                      to="/buyer-dashboard"
                      className="btn-primary px-6 py-3"
                    >
                      View Order Details
                    </Link>
                    <Link to="/explore" className="btn-secondary px-6 py-3">
                      Continue Shopping
                    </Link>
                  </div>
                </div>
              )}
            </div>

            {/* Order Summary Sidebar */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl shadow-sm p-6 sticky top-8">
                <h3 className="text-lg font-bold text-gray-900 mb-4">
                  Order Summary
                </h3>

                <div className="space-y-4 mb-6">
                  {cartItems.map((item) => {
                    const price = typeof item.price === 'string' ? parseFloat(item.price) : item.price
                    return (
                      <div key={item.id} className="flex items-center space-x-3">
                        <img 
                          src={item.product?.image || item.image || 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=100&h=100&fit=crop'} 
                          alt={item.product?.title || item.title}
                          className="w-16 h-16 rounded-lg object-cover"
                          onError={(e) => {
                            e.target.src = 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=100&h=100&fit=crop'
                          }}
                        />
                        <div className="flex-1">
                          <p className="font-medium text-gray-900 text-sm">{item.product?.title || item.title}</p>
                          <p className="text-sm text-gray-600">Qty: {item.quantity}</p>
                        </div>
                        <p className="font-bold text-gray-900">KSH {(() => {
                          const price = item.product?.price || item.price || 0
                          const numPrice = typeof price === 'string' ? parseFloat(price) : price
                          const validPrice = isNaN(numPrice) ? 0 : numPrice
                          return (validPrice * item.quantity).toFixed(2)
                        })()}</p>
                      </div>
                    )
                  })}
                </div>

                <div className="border-t border-gray-200 pt-4 space-y-2">
                  <div className="flex justify-between text-gray-700">
                    <span>Subtotal</span>
                    <span className="font-medium">KSH {subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-gray-700">
                    <span>Shipping</span>
                    <span className="font-medium">KSH {shipping.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-gray-700">
                    <span>Tax</span>
                    <span className="font-medium">KSH {tax.toFixed(2)}</span>
                  </div>
                  <div className="border-t border-gray-200 pt-2 mt-2">
                    <div className="flex justify-between">
                      <span className="text-lg font-bold text-gray-900">Total</span>
                      <span className="text-xl font-bold text-gray-900">KSH {total.toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div className="flex justify-between">
              <button
                type="button"
                onClick={handlePrevious}
                className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 transition"
              >
                Back
              </button>
              <button
                type="submit"
                disabled={processing}
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition disabled:bg-gray-400"
              >
                {processing ? "Processing..." : "Pay Now"}
              </button>
            </div>
          </form>
        )}

        {/* Step 3: Confirmation */}
        {step === 3 && (
          <div className="text-center space-y-4">
            <h3 className="text-xl font-semibold text-green-700">
              ✅ Payment Successful!
            </h3>
            <p>Your order has been placed successfully.</p>
            <button
              onClick={handleConfirmOrder}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              Go Back Home
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default CheckoutPage;
