
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

function BuyerDashboard() {
  const [activeTab, setActiveTab] = useState("orders");

  // Mock data
  const orders = [
    {
      id: "#1234",
      product: "Ceramic Vase",
      artisan: "Sarah Johnson",
      price: 45.0,
      status: "Delivered",
      date: "2025-10-10",
      image:
        "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=100&h=100&fit=crop",
      canReview: true,
    },
    {
      id: "#1233",
      product: "Wood Carving",
      artisan: "John Smith",
      price: 120.0,
      status: "In Transit",
      date: "2025-10-14",
      image:
        "https://images.unsplash.com/photo-1551522435-a13afa10f103?w=100&h=100&fit=crop",
      canReview: false,
    },
    {
      id: "#1232",
      product: "Textile Art",
      artisan: "Maria Garcia",
      price: 85.0,
      status: "Processing",
      date: "2025-10-15",
      image:
        "https://images.unsplash.com/photo-1558769132-cb1aea3c8565?w=100&h=100&fit=crop",
      canReview: false,
    },
  ];

  const messages = [
    {
      id: 1,
      artisan: "Sarah Johnson",
      lastMessage:
        "Thank you for your purchase! Let me know if you need anything.",
      time: "2 hours ago",
      unread: true,
    },
    {
      id: 2,
      artisan: "John Smith",
      lastMessage: "Your order has been shipped!",
      time: "1 day ago",
      unread: false,
    },
    {
      id: 3,
      artisan: "Maria Garcia",
      lastMessage: "I can customize that piece for you.",
      time: "3 days ago",
      unread: false,
    },
  ];

  const collections = [
    {
      id: 1,
      name: "Favorites",
      itemCount: 12,
      image:
        "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=200&h=200&fit=crop",
    },
    {
      id: 2,
      name: "Wishlist",
      itemCount: 8,
      image:
        "https://images.unsplash.com/photo-1551522435-a13afa10f103?w=200&h=200&fit=crop",
    },
    {
      id: 3,
      name: "Gift Ideas",
      itemCount: 5,
      image:
        "https://images.unsplash.com/photo-1558769132-cb1aea3c8565?w=200&h=200&fit=crop",
    },
  ];

  const paymentHistory = [
    {
      id: 1,
      orderId: "#1234",
      amount: 45.0,
      date: "2025-10-10",
      method: "Credit Card",
      status: "Completed",
    },
    {
      id: 2,
      orderId: "#1233",
      amount: 120.0,
      date: "2025-10-14",
      method: "PayPal",
      status: "Completed",
    },
    {
      id: 3,
      orderId: "#1232",
      amount: 85.0,
      date: "2025-10-15",
      method: "Credit Card",
      status: "Pending",
    },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case "Delivered":
      case "Completed":
        return "bg-green-100 text-green-800";
      case "In Transit":
        return "bg-blue-100 text-blue-800";
      case "Processing":
      case "Pending":
        return "bg-yellow-100 text-yellow-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <Diamond className="w-6 h-6 text-primary" fill="currentColor" />
              <span className="text-xl font-bold text-gray-900">
                SokoDigital
              </span>
            </Link>

            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100">
                <Bell className="w-5 h-5" />
              </button>
              <button className="flex items-center space-x-2 p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100">
                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                  <User className="w-5 h-5 text-white" />
                </div>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex flex-col md:flex-row">
        {/* Sidebar */}
        <aside className="w-full md:w-64 bg-white border-b md:border-b-0 md:border-r border-gray-200">
          <div className="p-4 overflow-x-auto">
            <h2 className="text-sm font-semibold text-gray-500 uppercase mb-4">
              Buyer Dashboard
            </h2>
            <nav className="flex md:flex-col space-x-2 md:space-x-0 md:space-y-1 overflow-x-auto md:overflow-x-visible pb-2 md:pb-0">
              <button
                onClick={() => setActiveTab("dashboard")}
                className={`flex-shrink-0 md:w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === "dashboard"
                    ? "bg-gray-100 text-gray-900"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                <LayoutDashboard className="w-5 h-5" />
                <span className="font-medium">Dashboard</span>
              </button>

              <button
                onClick={() => setActiveTab("orders")}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors ${
                  activeTab === "orders"
                    ? "bg-primary/10 text-primary"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                <ShoppingBag className="w-5 h-5" />
                <span className="font-medium">My Orders</span>
              </button>

              <button
                onClick={() => setActiveTab("messages")}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors ${
                  activeTab === "messages"
                    ? "bg-gray-100 text-gray-900"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                <MessageSquare className="w-5 h-5" />
                <span className="font-medium">Messages</span>
              </button>

              <button
                onClick={() => setActiveTab("collections")}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors ${
                  activeTab === "collections"
                    ? "bg-gray-100 text-gray-900"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                <Heart className="w-5 h-5" />
                <span className="font-medium">Collections</span>
              </button>

              <button
                onClick={() => setActiveTab("payments")}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors ${
                  activeTab === "payments"
                    ? "bg-gray-100 text-gray-900"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                <CreditCard className="w-5 h-5" />
                <span className="font-medium">Payment History</span>
              </button>
            </nav>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          <div className="max-w-5xl">
            {/* Dashboard Overview */}
            {activeTab === "dashboard" && (
              <>
                <h1 className="text-3xl font-bold text-gray-900 mb-8">
                  Dashboard Overview
                </h1>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-sm font-medium text-gray-600">
                        Total Orders
                      </h3>
                      <ShoppingBag className="w-5 h-5 text-primary" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900">
                      {orders.length}
                    </p>
                  </div>
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-sm font-medium text-gray-600">
                        Collections
                      </h3>
                      <Heart className="w-5 h-5 text-primary" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900">
                      {collections.length}
                    </p>
                  </div>
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-sm font-medium text-gray-600">
                        Messages
                      </h3>
                      <MessageSquare className="w-5 h-5 text-primary" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900">
                      {messages.length}
                    </p>
                  </div>
                </div>

                <div className="card p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">
                    Recent Orders
                  </h2>
                  <div className="space-y-4">
                    {orders.slice(0, 3).map((order) => (
                      <div
                        key={order.id}
                        className="flex items-center justify-between py-3 border-b border-gray-100 last:border-0"
                      >
                        <div className="flex items-center space-x-4">
                          <img
                            src={order.image}
                            alt={order.product}
                            className="w-12 h-12 rounded-lg object-cover"
                          />
                          <div>
                            <p className="font-medium text-gray-900">
                              {order.product}
                            </p>
                            <p className="text-sm text-gray-600">
                              Order {order.id}
                            </p>
                          </div>
                        </div>
                        <span
                          className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(
                            order.status
                          )}`}
                        >
                          {order.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}

            {/* Orders Tab */}
            {activeTab === "orders" && (
              <>
                <h1 className="text-3xl font-bold text-gray-900 mb-8">
                  My Orders
                </h1>
                <div className="space-y-4">
                  {orders.map((order) => (
                    <div key={order.id} className="card p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-start space-x-4">
                          <img
                            src={order.image}
                            alt={order.product}
                            className="w-20 h-20 rounded-lg object-cover"
                          />
                          <div>
                            <h3 className="font-bold text-gray-900 text-lg">
                              {order.product}
                            </h3>
                            <p className="text-sm text-gray-600 mb-1">
                              by {order.artisan}
                            </p>
                            <p className="text-sm text-gray-500">
                              Order {order.id} • {order.date}
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-xl font-bold text-gray-900 mb-2">
                            ${order.price.toFixed(2)}
                          </p>
                          <span
                            className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(
                              order.status
                            )}`}
                          >
                            {order.status}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3 pt-4 border-t border-gray-200">
                        <Link
                          to={`/product/${order.id}`}
                          className="btn-secondary text-sm px-4 py-2"
                        >
                          View Product
                        </Link>
                        {order.canReview && (
                          <button className="btn-primary text-sm px-4 py-2">
                            Write Review
                          </button>
                        )}
                        <Link
                          to={`/messages/${order.id}`}
                          className="btn-secondary text-sm px-4 py-2"
                        >
                          Message Artisan
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}

            {/* Messages Tab */}
            {activeTab === "messages" && (
              <>
                <h1 className="text-3xl font-bold text-gray-900 mb-8">
                  Messages
                </h1>
                <div className="space-y-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className="card p-6 hover:shadow-md transition-shadow cursor-pointer"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-4">
                          <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center">
                            <User className="w-6 h-6 text-white" />
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-1">
                              <h3 className="font-bold text-gray-900">
                                {message.artisan}
                              </h3>
                              {message.unread && (
                                <span className="w-2 h-2 bg-primary rounded-full"></span>
                              )}
                            </div>
                            <p className="text-sm text-gray-700">
                              {message.lastMessage}
                            </p>
                          </div>
                        </div>
                        <span className="text-xs text-gray-500">
                          {message.time}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}

            {/* Collections Tab */}
            {activeTab === "collections" && (
              <>
                <div className="flex items-center justify-between mb-8">
                  <h1 className="text-3xl font-bold text-gray-900">
                    My Collections
                  </h1>
                  <button className="btn-primary px-4 py-2">
                    Create Collection
                  </button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {collections.map((collection) => (
                    <Link
                      key={collection.id}
                      to={`/collection/${collection.id}`}
                      className="card group cursor-pointer hover:shadow-lg transition-shadow"
                    >
                      <div className="aspect-square overflow-hidden">
                        <img
                          src={collection.image}
                          alt={collection.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                      </div>
                      <div className="p-5">
                        <h3 className="text-lg font-bold text-gray-900 mb-1">
                          {collection.name}
                        </h3>
                        <p className="text-sm text-gray-600">
                          {collection.itemCount} items
                        </p>
                      </div>
                    </Link>
                  ))}
                </div>
              </>
            )}

            {/* Payment History Tab */}
            {activeTab === "payments" && (
              <>
                <h1 className="text-3xl font-bold text-gray-900 mb-8">
                  Payment History
                </h1>
                <div className="card overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-gray-50 border-b border-gray-200">
                        <tr>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                            Order ID
                          </th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                            Date
                          </th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                            Method
                          </th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                            Amount
                          </th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                            Status
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200">
                        {paymentHistory.map((payment) => (
                          <tr key={payment.id} className="hover:bg-gray-50">
                            <td className="px-6 py-4 text-sm font-medium text-gray-900">
                              {payment.orderId}
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-600">
                              {payment.date}
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-600">
                              {payment.method}
                            </td>
                            <td className="px-6 py-4 text-sm font-bold text-gray-900">
                              ${payment.amount.toFixed(2)}
                            </td>
                            <td className="px-6 py-4">
                              <span
                                className={`px-3 py-1 text-xs font-medium rounded-full ${getStatusColor(
                                  payment.status
                                )}`}
                              >
                                {payment.status}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

export default BuyerDashboard;
