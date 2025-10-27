import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Diamond, LayoutDashboard, Package, ShoppingBag, MessageSquare, Upload, Bell, User, Plus } from 'lucide-react'
import { api } from '../services/api'

const ArtisanDashboard = () => {
  const [activeTab, setActiveTab] = useState('products')
  const [showAddProduct, setShowAddProduct] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const [uploadedImage, setUploadedImage] = useState(null)
  const [formData, setFormData] = useState({
    title: '',
    category: '',
    subcategory: '',
    description: '',
    price: ''
  })

  const [myProducts, setMyProducts] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      setLoading(true)
      const products = await api.products.getAll()
      setMyProducts(products)
    } catch (error) {
      console.error('Failed to load products:', error)
    } finally {
      setLoading(false)
    }
  }

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
      const file = e.dataTransfer.files[0]
      const reader = new FileReader()
      reader.onload = (e) => {
        setUploadedImage(e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      const reader = new FileReader()
      reader.onload = (e) => {
        setUploadedImage(e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    try {
      setLoading(true)
      const productData = {
        title: formData.title,
        description: formData.description,
        price: parseFloat(formData.price),
        stock: 10, // Default stock
        currency: 'USD'
      }
      
      await api.products.create(productData)
      await loadProducts() // Reload products
      
      setShowAddProduct(false)
      setFormData({ title: '', category: '', subcategory: '', description: '', price: '' })
      setUploadedImage(null)
      
      alert('Product added successfully!')
    } catch (error) {
      alert('Failed to add product: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (productId) => {
    if (confirm('Are you sure you want to delete this product?')) {
      try {
        setLoading(true)
        await api.products.delete(productId)
        await loadProducts() // Reload products
        alert('Product deleted successfully!')
      } catch (error) {
        alert('Failed to delete product: ' + error.message)
      } finally {
        setLoading(false)
      }
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <Diamond className="w-6 h-6 text-primary-600" fill="currentColor" />
              <span className="text-xl font-bold text-gray-900">SokoDigital</span>
            </Link>
            
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100">
                <Bell className="w-5 h-5" />
              </button>
              <button className="flex items-center space-x-2 p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100">
                <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
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
                onClick={() => { setActiveTab('products'); setShowAddProduct(false); }}
                className={`flex-shrink-0 md:w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors whitespace-nowrap ${
                  activeTab === 'products'
                    ? 'bg-primary-600/10 text-primary-600'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <Package className="w-5 h-5" />
                <span className="font-medium">My Products</span>
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
                      <Package className="w-5 h-5 text-primary-600" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900">{myProducts.length}</p>
                  </div>
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-sm font-medium text-gray-600">Total Orders</h3>
                      <ShoppingBag className="w-5 h-5 text-primary-600" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900">28</p>
                  </div>
                  <div className="card p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-sm font-medium text-gray-600">Revenue</h3>
                      <span className="text-primary-600 font-bold">KSH</span>
                    </div>
                    <p className="text-3xl font-bold text-gray-900">KSH 2,450</p>
                  </div>
                </div>
              </>
            )}

            {activeTab === 'products' && !showAddProduct && (
              <>
                <div className="flex items-center justify-between mb-8">
                  <h1 className="text-3xl font-bold text-gray-900">
                    My Products ({myProducts.length})
                  </h1>
                  <button
                    onClick={() => setShowAddProduct(true)}
                    className="btn-primary px-6 py-3 flex items-center space-x-2"
                  >
                    <Plus className="w-5 h-5" />
                    <span>Add Product</span>
                  </button>
                </div>

                {myProducts.length === 0 ? (
                  <div className="card p-12 text-center">
                    <Package className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-gray-900 mb-2">No products yet</h3>
                    <p className="text-gray-600 mb-6">Start by adding your first product</p>
                    <button
                      onClick={() => setShowAddProduct(true)}
                      className="btn-primary px-6 py-3 inline-flex items-center space-x-2"
                    >
                      <Plus className="w-5 h-5" />
                      <span>Add Your First Product</span>
                    </button>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {myProducts.map((product) => (
                      <div key={product.id} className="card p-6">
                        <div className="flex items-start space-x-4">
                          <img 
                            src={product.image} 
                            alt={product.title}
                            className="w-20 h-20 rounded-lg object-cover"
                          />
                          <div className="flex-1">
                            <h3 className="font-bold text-gray-900 mb-1">{product.title}</h3>
                            <p className="text-lg font-bold text-gray-900 mb-2">KSH {product.price.toFixed(2)}</p>
                            <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                              {product.status}
                            </span>
                          </div>
                        </div>
                        <div className="flex items-center space-x-3 mt-4 pt-4 border-t border-gray-200">
                          <button className="btn-secondary text-sm px-4 py-2 flex-1">
                            Edit
                          </button>
                          <button 
                            onClick={() => handleDelete(product.id)}
                            className="btn-secondary text-sm px-4 py-2 flex-1 text-red-600 hover:bg-red-50"
                            disabled={loading}
                          >
                            {loading ? 'Deleting...' : 'Delete'}
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}

            {activeTab === 'products' && showAddProduct && (
              <>
                <div className="flex items-center justify-between mb-8">
                  <h1 className="text-3xl font-bold text-gray-900">
                    Add New Product
                  </h1>
                  <button
                    onClick={() => setShowAddProduct(false)}
                    className="btn-secondary px-4 py-2"
                  >
                    Cancel
                  </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
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
                          ? 'border-primary-600 bg-primary-600/5'
                          : 'border-gray-300 hover:border-gray-400'
                      }`}
                    >
                      {uploadedImage ? (
                        <div className="space-y-4">
                          <img src={uploadedImage} alt="Preview" className="w-32 h-32 object-cover rounded-lg mx-auto" />
                          <button
                            type="button"
                            onClick={() => setUploadedImage(null)}
                            className="text-sm text-red-600 hover:text-red-700"
                          >
                            Remove Image
                          </button>
                        </div>
                      ) : (
                        <>
                          <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                          <div className="mb-2">
                            <label htmlFor="file-upload" className="cursor-pointer">
                              <span className="text-primary-600 hover:text-primary-700 font-medium">
                                Click to upload
                              </span>
                              <span className="text-gray-600"> or drag and drop</span>
                            </label>
                            <input
                              id="file-upload"
                              type="file"
                              className="hidden"
                              onChange={handleFileInput}
                              accept=".png,.jpg,.jpeg,.gif"
                            />
                          </div>
                          <p className="text-sm text-gray-500">
                            PNG, JPG or GIF (MAX. 800x400px)
                          </p>
                        </>
                      )}
                    </div>
                  </div>

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

                  <div>
                    <label htmlFor="price" className="block text-sm font-medium text-gray-700 mb-2">
                      Price (KSH)
                    </label>
                    <div className="relative">
                      <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">
                        KSH
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
                        className="input-field pl-16"
                        required
                      />
                    </div>
                  </div>

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
                      <span className="font-bold text-gray-900">KSH 45.00</span>
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
                        <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
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
