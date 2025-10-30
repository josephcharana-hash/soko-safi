import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const CheckoutPage = () => {
  const [step, setStep] = useState(1); // 1: Shipping, 2: Payment, 3: Confirmation
  const [processing, setProcessing] = useState(false);
  const navigate = useNavigate();

  const [shippingInfo, setShippingInfo] = useState({
    fullName: "",
    address: "",
    city: "",
    phone: "",
  });

  const [paymentInfo, setPaymentInfo] = useState({
    method: "mpesa", // default payment method
    mpesaNumber: "",
  });

  const handleShippingChange = (e) => {
    const { name, value } = e.target;
    setShippingInfo({ ...shippingInfo, [name]: value });
  };

  const handlePaymentChange = (e) => {
    const { name, value } = e.target;
    setPaymentInfo({ ...paymentInfo, [name]: value });
  };

  const handleNext = () => setStep(step + 1);
  const handlePrevious = () => setStep(step - 1);

  const handlePayment = async (e) => {
    e.preventDefault();
    setProcessing(true);

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
            <button
              type="button"
              onClick={handleNext}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
            >
              Continue to Payment
            </button>
          </form>
        )}

        {/* Step 2: Payment */}
        {step === 2 && (
          <form onSubmit={handlePayment} className="space-y-4">
            <div>
              <label className="block text-sm font-medium">Payment Method</label>
              <select
                name="method"
                value={paymentInfo.method}
                onChange={handlePaymentChange}
                className="mt-1 w-full border border-gray-300 rounded-lg p-2"
              >
                <option value="mpesa">M-Pesa</option>
                <option value="card">Credit/Debit Card</option>
              </select>
            </div>

            {paymentInfo.method === "mpesa" && (
              <div>
                <label className="block text-sm font-medium">M-Pesa Number</label>
                <input
                  type="text"
                  name="mpesaNumber"
                  value={paymentInfo.mpesaNumber}
                  onChange={handlePaymentChange}
                  className="mt-1 w-full border border-gray-300 rounded-lg p-2"
                  placeholder="07XX XXX XXX"
                  required
                />
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

