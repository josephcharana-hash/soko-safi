import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Diamond, LayoutDashboard, Package, ShoppingBag, MessageSquare, Upload, Bell, User } from 'lucide-react'

const ArtisanDashboard = () => {
  const [activeTab, setActiveTab] = useState('products')
  const [dragActive, setDragActive] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    category: '',
    subcategory: '',
    description: '',
    price: ''
  })

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      // Handle file upload
      console.log('File dropped:', e.dataTransfer.files[0])
    }
  }

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      // Handle file upload
      console.log('File selected:', e.target.files[0])
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Product submitted:', formData)
    // Handle product submission
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <Diamond className="w-6 h-6 text-primary" fill="currentColor" />
              <span className="text-xl font-bold text-gray-900">SokoDigital</span>
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
              Artisan Dashboard
            </h2>
            <nav className="flex md:flex-col space-x-2 md:space-x-0 md:space-y-1 overflow-x-auto md:overflow-x-visible pb-2 md:pb-0">
              <button
                onClick={() => setActiveTab('dashboard')}
                className={`flex-shrink-0 md:w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === 'dashboard'
                    ? 'bg-gray-100 text-gray-900'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <LayoutDashboard className="w-5 h-5" />
                <span className="font-medium">Dashboard</span>
              </button>
              
              <button
                onClick={() => setActiveTab('products')}
                className={`flex-shrink-0 md:w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === 'products'
                    ? 'bg-primary/10 text-primary'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <Package className="w-5 h-5" />
                <span className="font-medium">Products</span>
              </button>
              
              <button
                onClick={() => setActiveTab('orders')}
                className={`flex-shrink-0 md:w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === 'orders'
                    ? 'bg-gray-100 text-gray-900'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <ShoppingBag className="w-5 h-5" />
                <span className="font-medium">Orders</span>
              </button>
              
              <button
                onClick={() => setActiveTab('messages')}
                className={`flex-shrink-0 md:w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === 'messages'
                    ? 'bg-gray-100 text-gray-900'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <MessageSquare className="w-5 h-5" />
                <span className="font-medium">Messages</span>
              </button>
            </nav>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          <div className="max-w-4xl">
            {activeTab === 'dashboard' && (
              <>
                <h1 className="text-3xl font-bold text-gray-900 mb-8">
                  Dashboard Overview
                </h1>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-sm font-medium text-gray-600">Total Products</h3>
                      <Package className="w-5 h-5 text-primary" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900">12</p>
                  </div>
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-sm font-medium text-gray-600">Total Orders</h3>
                      <ShoppingBag className="w-5 h-5 text-primary" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900">28</p>
                  </div>
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-sm font-medium text-gray-600">Revenue</h3>
                      <span className="text-primary font-bold">$</span>
                    </div>
                    <p className="text-3xl font-bold text-gray-900">$2,450</p>
                  </div>
                </div>
                <div className="card p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Activity</h2>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between py-3 border-b border-gray-100">
                      <div>
                        <p className="font-medium text-gray-900">New order received</p>
                        <p className="text-sm text-gray-600">Ceramic Vase - $45.00</p>
                      </div>
                      <span className="text-sm text-gray-500">2 hours ago</span>
                    </div>
                    <div className="flex items-center justify-between py-3 border-b border-gray-100">
                      <div>
                        <p className="font-medium text-gray-900">Product viewed</p>
                        <p className="text-sm text-gray-600">Wood Carving - 15 views</p>
                      </div>
                      <span className="text-sm text-gray-500">5 hours ago</span>
                    </div>
                    <div className="flex items-center justify-between py-3">
                      <div>
                        <p className="font-medium text-gray-900">New message</p>
                        <p className="text-sm text-gray-600">Question about Textile Art</p>
                      </div>
                      <span className="text-sm text-gray-500">1 day ago</span>
                    </div>
                  </div>
                </div>
              </>
            )}

            {activeTab === 'products' && (
              <>
                <h1 className="text-3xl font-bold text-gray-900 mb-8">
                  Upload Your Work
                </h1>

                <form onSubmit={handleSubmit} className="space-y-6">
              {/* Product Image Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Product Image
                </label>
                <div
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                  className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
                    dragActive
                      ? 'border-primary bg-primary/5'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <div className="mb-2">
                    <label htmlFor="file-upload" className="cursor-pointer">
                      <span className="text-primary hover:text-primary-hover font-medium">
                        Click to upload
                      </span>
                      <span className="text-gray-600"> or drag and drop</span>
                    </label>
                    <input
                      id="file-upload"
                      type="file"
                      className="hidden"
                      onChange={handleFileInput}
                      accept=".svg,.png,.jpg,.jpeg,.gif"
                    />
                  </div>
                  <p className="text-sm text-gray-500">
                    SVG, PNG, JPG or GIF (MAX. 800x400px)
                  </p>
                </div>
              </div>

              {/* Title */}
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                  Title
                </label>
                <input
                  type="text"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="e.g., Handcrafted Wooden Bowl"
                  className="input-field"
                  required
                />
              </div>

              {/* Category and Subcategory */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                    Category
                  </label>
                  <select
                    id="category"
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="">Select category</option>
                    <option value="ceramics">Ceramics</option>
                    <option value="textiles">Textiles</option>
                    <option value="woodwork">Woodwork</option>
                    <option value="jewelry">Jewelry</option>
                    <option value="painting">Painting</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="subcategory" className="block text-sm font-medium text-gray-700 mb-2">
                    Subcategory
                  </label>
                  <select
                    id="subcategory"
                    name="subcategory"
                    value={formData.subcategory}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="">Select subcategory</option>
                    <option value="functional">Functional</option>
                    <option value="decorative">Decorative</option>
                    <option value="wearable">Wearable</option>
                  </select>
                </div>
              </div>

              {/* Description */}
              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Describe your masterpiece..."
                  rows={5}
                  className="input-field resize-none"
                  required
                />
              </div>

              {/* Price */}
              <div>
                <label htmlFor="price" className="block text-sm font-medium text-gray-700 mb-2">
                  Price
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">
                    $
                  </span>
                  <input
                    type="number"
                    id="price"
                    name="price"
                    value={formData.price}
                    onChange={handleChange}
                    placeholder="0.00"
                    step="0.01"
                    min="0"
                    className="input-field pl-8"
                    required
                  />
                </div>
              </div>

              {/* Submit Button */}
              <div className="flex justify-end pt-4">
                <button
                  type="submit"
                  className="btn-primary px-8 py-3"
                >
                  Submit Product
                </button>
              </div>
            </form>
              </>
            )}

            {activeTab === 'orders' && (
              <>
                <h1 className="text-3xl font-bold text-gray-900 mb-8">
                  Orders
                </h1>
                <div className="space-y-4">
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h3 className="font-bold text-gray-900">Order #1234</h3>
                        <p className="text-sm text-gray-600">Ceramic Vase</p>
                      </div>
                      <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
                        Completed
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Customer: John Doe</span>
                      <span className="font-bold text-gray-900">$45.00</span>
                    </div>
                  </div>
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h3 className="font-bold text-gray-900">Order #1233</h3>
                        <p className="text-sm text-gray-600">Wood Carving</p>
                      </div>
                      <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm font-medium rounded-full">
                        Processing
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Customer: Jane Smith</span>
                      <span className="font-bold text-gray-900">$120.00</span>
                    </div>
                  </div>
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h3 className="font-bold text-gray-900">Order #1232</h3>
                        <p className="text-sm text-gray-600">Textile Art</p>
                      </div>
                      <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
                        Pending
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Customer: Mike Johnson</span>
                      <span className="font-bold text-gray-900">$85.00</span>
                    </div>
                  </div>
                </div>
              </>
            )}

            {activeTab === 'messages' && (
              <>
                <h1 className="text-3xl font-bold text-gray-900 mb-8">
                  Messages
                </h1>
                <div className="space-y-4">
                  <div className="card p-6 hover:shadow-md transition-shadow cursor-pointer">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center">
                          <User className="w-5 h-5 text-white" />
                        </div>
                        <div>
                          <h3 className="font-bold text-gray-900">Sarah Williams</h3>
                          <p className="text-sm text-gray-600">Question about Ceramic Vase</p>
                        </div>
                      </div>
                      <span className="text-xs text-gray-500">10 min ago</span>
                    </div>
                    <p className="text-sm text-gray-700 ml-13">
                      Hi! I'm interested in the ceramic vase. Do you ship internationally?
                    </p>
                  </div>
                  <div className="card p-6 hover:shadow-md transition-shadow cursor-pointer">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gray-400 rounded-full flex items-center justify-center">
                          <User className="w-5 h-5 text-white" />
                        </div>
                        <div>
                          <h3 className="font-bold text-gray-900">David Brown</h3>
                          <p className="text-sm text-gray-600">Custom order inquiry</p>
                        </div>
                      </div>
                      <span className="text-xs text-gray-500">2 hours ago</span>
                    </div>
                    <p className="text-sm text-gray-700 ml-13">
                      Can you create a custom wood carving? I have a specific design in mind.
                    </p>
                  </div>
                  <div className="card p-6 hover:shadow-md transition-shadow cursor-pointer">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gray-400 rounded-full flex items-center justify-center">
                          <User className="w-5 h-5 text-white" />
                        </div>
                        <div>
                          <h3 className="font-bold text-gray-900">Emily Davis</h3>
                          <p className="text-sm text-gray-600">Thank you message</p>
                        </div>
                      </div>
                      <span className="text-xs text-gray-500">1 day ago</span>
                    </div>
                    <p className="text-sm text-gray-700 ml-13">
                      Thank you so much! The textile art arrived safely and it's beautiful!
                    </p>
                  </div>
                </div>
              </>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

export default ArtisanDashboard