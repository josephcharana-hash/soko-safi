<<<<<<< HEAD
import { Link } from "react-router-dom";
import Navbar from "../Components/Layout/Navbar";
import Footer from "../Components/Layout/Footer";

const ExplorePage = () => {
  const works = [
    {
      id: 1,
      title: "Ceramic Vase",
      description: "Handcrafted ceramic vase with a unique glaze.",
      price: 45.0,
      image:
        "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=400&h=400&fit=crop",
    },
    {
      id: 2,
      title: "Woven Basket",
      description: "Woven basket with intricate patterns and natural dyes.",
      price: 32.0,
      image:
        "https://images.unsplash.com/photo-1595429426858-28f04f7db1f5?w=400&h=400&fit=crop",
    },
    {
      id: 3,
      title: "Wood Carving",
      description: "Detailed wood carving of a native animal.",
      price: 120.0,
      image:
        "https://images.unsplash.com/photo-1551522435-a13afa10f103?w=400&h=400&fit=crop",
    },
    {
      id: 4,
      title: "Textile Art",
      description: "Colorful textile art piece depicting a local scene.",
      price: 85.0,
      image:
        "https://images.unsplash.com/photo-1558769132-cb1aea3c8565?w=400&h=400&fit=crop",
    },
    {
      id: 5,
      title: "Pottery Bowl",
      description: "Beautiful handmade pottery bowl.",
      price: 38.0,
      image:
        "https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=400&h=400&fit=crop",
    },
    {
      id: 6,
      title: "Macrame Wall Hanging",
      description: "Intricate macrame wall decoration.",
      price: 65.0,
      image:
        "https://images.unsplash.com/photo-1615529182904-14819c35db37?w=400&h=400&fit=crop",
    },
  ];
=======
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Search, Filter, Grid, List, Heart, Star, MapPin, Clock } from 'lucide-react'
import Navbar from '../Components/Layout/Navbar'
import Footer from '../Components/Layout/Footer'
import LazyImage from '../Components/LazyImage'
import LoadingSpinner from '../Components/LoadingSpinner'
import { api } from '../services/api'

const ExplorePage = () => {
  const [viewMode, setViewMode] = useState('grid')
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [sortBy, setSortBy] = useState('featured')
  const [showFilters, setShowFilters] = useState(false)
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [categories, setCategories] = useState([])

  // Categories will be loaded from API

  // Products will be loaded from API

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)
        
        const [productsResponse, categoriesResponse] = await Promise.all([
          api.products.getAll(),
          api.categories.getAll()
        ])

        const productsArray = Array.isArray(productsResponse) ? productsResponse : []
        setProducts(productsArray)
        
        // Build categories with product counts
        const categoryMap = new Map()
        productsArray.forEach(product => {
          const category = product.category || 'other'
          categoryMap.set(category, (categoryMap.get(category) || 0) + 1)
        })
        
        const categoriesWithCounts = [
          { id: 'all', name: 'All Categories', count: productsArray.length },
          ...categoriesResponse.map(cat => ({
            id: cat.id,
            name: cat.name,
            count: categoryMap.get(cat.id) || 0
          }))
        ]
        
        setCategories(categoriesWithCounts)
      } catch (error) {
        console.error('Failed to fetch data:', error)
        setError('Failed to load products. Please try again later.')
        
        // Use fallback data from API service
        const fallbackProducts = await api.products.getAll().catch(() => [])
        const fallbackCategories = await api.categories.getAll().catch(() => [])
        
        setProducts(fallbackProducts)
        setCategories([
          { id: 'all', name: 'All Categories', count: fallbackProducts.length },
          ...fallbackCategories.map(cat => ({ ...cat, count: 0 }))
        ])
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const filteredWorks = products.filter(work => {
    const matchesSearch = work.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         work.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         work.artisan_name?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || work.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const sortedWorks = [...filteredWorks].sort((a, b) => {
    switch (sortBy) {
      case 'price-low':
        return (a.price || 0) - (b.price || 0)
      case 'price-high':
        return (b.price || 0) - (a.price || 0)
      case 'rating':
        return (b.rating || 0) - (a.rating || 0)
      case 'newest':
        return new Date(b.created_at || 0) - new Date(a.created_at || 0)
      default:
        return 0
    }
  })
>>>>>>> c528bbd7c7c448457de4473c0be34a9199288a97

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />

<<<<<<< HEAD
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Explore Artisan Works
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Discover unique handcrafted pieces from talented local artisans
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {works.map((work) => (
              <Link
                key={work.id}
                to={`/product/${work.id}`}
                className="card group cursor-pointer hover:shadow-lg transition-shadow duration-300"
              >
                <div className="aspect-square overflow-hidden">
                  <img
=======
      <main className="flex-1 pt-20">
        {/* Hero Section */}
        <section className="bg-gradient-to-r from-primary-600 to-primary-700 text-white py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">
                Discover Artisan Treasures
              </h1>
              <p className="text-xl text-primary-100 max-w-2xl mx-auto mb-8">
                Explore unique handcrafted pieces from talented Kenyan artisans across the country
              </p>

              {/* Search Bar */}
              <div className="max-w-2xl mx-auto relative">
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    type="text"
                    placeholder="Search for artisans, products, or categories..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-12 pr-4 py-4 rounded-xl text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-300 text-lg"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Filters and Controls */}
          <div className="bg-white rounded-2xl shadow-sm p-6 mb-8">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
              {/* Categories */}
              <div className="flex flex-wrap gap-2">
                {categories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => setSelectedCategory(category.id)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                      selectedCategory === category.id
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {category.name} ({category.count})
                  </button>
                ))}
              </div>

              {/* Controls */}
              <div className="flex items-center gap-4">
                {/* Sort */}
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="featured">Featured</option>
                  <option value="newest">Newest</option>
                  <option value="price-low">Price: Low to High</option>
                  <option value="price-high">Price: High to Low</option>
                  <option value="rating">Highest Rated</option>
                </select>

                {/* View Mode */}
                <div className="flex border border-gray-300 rounded-lg">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`p-2 ${viewMode === 'grid' ? 'bg-primary-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
                  >
                    <Grid className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`p-2 ${viewMode === 'list' ? 'bg-primary-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
                  >
                    <List className="w-5 h-5" />
                  </button>
                </div>

                {/* Filter Toggle */}
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  <Filter className="w-4 h-4" />
                  Filters
                </button>
              </div>
            </div>

            {/* Advanced Filters */}
            {showFilters && (
              <div className="mt-6 pt-6 border-t border-gray-200">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Price Range</label>
                    <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                      <option>All Prices</option>
                      <option>Under KSh 1,000</option>
                      <option>KSh 1,000 - 2,500</option>
                      <option>KSh 2,500 - 5,000</option>
                      <option>Over KSh 5,000</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                    <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                      <option>All Locations</option>
                      <option>Nairobi</option>
                      <option>Eldoret</option>
                      <option>Kisumu</option>
                      <option>Nakuru</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Rating</label>
                    <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                      <option>Any Rating</option>
                      <option>4.5+ Stars</option>
                      <option>4+ Stars</option>
                      <option>3+ Stars</option>
                    </select>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Results Count */}
          <div className="flex items-center justify-between mb-6">
            <p className="text-gray-600">
              {loading ? 'Loading products...' : `Showing ${sortedWorks.length} of ${products.length} products`}
            </p>
          </div>

          {/* Products Grid/List */}
          <div className={`${
            viewMode === 'grid'
              ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'
              : 'space-y-4'
          }`}>
            {sortedWorks.map((work) => (
              <Link
                key={work.id}
                to={`/product/${work.id}`}
                className={`group bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 overflow-hidden ${
                  viewMode === 'list' ? 'flex' : ''
                }`}
              >
                <div className={`relative ${viewMode === 'list' ? 'w-48 flex-shrink-0' : 'aspect-square'} overflow-hidden`}>
                  <LazyImage
>>>>>>> c528bbd7c7c448457de4473c0be34a9199288a97
                    src={work.image}
                    alt={work.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                  {work.isNew && (
                    <div className="absolute top-3 left-3 bg-primary-600 text-white text-xs font-semibold px-2 py-1 rounded-full">
                      New
                    </div>
                  )}
                  {work.originalPrice && (
                    <div className="absolute top-3 right-3 bg-red-500 text-white text-xs font-semibold px-2 py-1 rounded-full">
                      Sale
                    </div>
                  )}
                  <button className="absolute top-3 right-3 p-2 bg-white/80 backdrop-blur-sm rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
                    <Heart className="w-4 h-4 text-gray-600 hover:text-red-500" />
                  </button>
                </div>

                <div className={`p-6 ${viewMode === 'list' ? 'flex-1' : ''}`}>
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors mb-1">
                        {work.title}
                      </h3>
                      <div className="flex items-center gap-2 text-sm text-gray-500 mb-2">
                        <MapPin className="w-3 h-3" />
                        <span>{work.location}</span>
                        <span>•</span>
                        <span>by {work.artisan}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      <span className="text-sm font-medium">{work.rating}</span>
                      <span className="text-sm text-gray-500">({work.reviews})</span>
                    </div>
                  </div>

                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {work.description}
                  </p>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl font-bold text-gray-900">
                        KSh {work.price?.toLocaleString() || 'N/A'}
                      </span>
                      {work.original_price && (
                        <span className="text-sm text-gray-500 line-through">
                          KSh {work.original_price.toLocaleString()}
                        </span>
                      )}
                    </div>
                    <span className={`text-sm font-medium px-3 py-1 rounded-full ${
                      work.in_stock !== false ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                      {work.in_stock !== false ? 'In Stock' : 'Out of Stock'}
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {/* Load More */}
          {sortedWorks.length > 0 && (
            <div className="text-center mt-12">
              <button className="bg-white border-2 border-primary-600 text-primary-600 font-semibold rounded-xl px-8 py-4 hover:bg-primary-600 hover:text-white transition-colors">
                Load More Products
              </button>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex justify-center py-16">
              <LoadingSpinner size="lg" text="Loading products..." />
            </div>
          )}

          {/* Error State */}
          {error && !loading && (
            <div className="text-center py-16">
              <div className="w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-12 h-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Failed to load products</h3>
              <p className="text-gray-600 mb-6">{error}</p>
              <button
                onClick={() => window.location.reload()}
                className="btn-primary"
              >
                Try Again
              </button>
            </div>
          )}

          {/* Empty State */}
          {!loading && !error && sortedWorks.length === 0 && (
            <div className="text-center py-16">
              <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Search className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No products found</h3>
              <p className="text-gray-600 mb-6">Try adjusting your search or filter criteria</p>
              <button
                onClick={() => {
                  setSearchTerm('')
                  setSelectedCategory('all')
                  setSortBy('featured')
                }}
                className="btn-primary"
              >
                Clear Filters
              </button>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ExplorePage;
