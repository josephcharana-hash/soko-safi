import { useState } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { Diamond, ShoppingCart, Heart, Star, MessageSquare, ArrowLeft, User } from 'lucide-react'
import Navbar from '../Components/Layout/Navbar'
import Footer from '../Components/Layout/Footer'

const ProductDetailPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [quantity, setQuantity] = useState(1)
  const [activeImage, setActiveImage] = useState(0)

  // Mock product data - replace with API call
  const product = {
    id: id,
    title: 'Handcrafted Ceramic Vase',
    price: 45.00,
    description: 'This beautiful ceramic vase is handcrafted with care using traditional techniques passed down through generations. Each piece is unique with its own character and charm. The glaze is food-safe and the vase is perfect for fresh or dried flowers.',
    category: 'Ceramics',
    subcategory: 'Decorative',
    images: [
      'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=800&h=800&fit=crop',
      'https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=800&h=800&fit=crop',
      'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=800&h=800&fit=crop'
    ],
    artisan: {
      id: 1,
      name: 'Sarah Johnson',
      avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop',
      rating: 4.8,
      totalReviews: 124
    },
    inStock: true,
    reviews: [
      {
        id: 1,
        user: 'John Doe',
        rating: 5,
        comment: 'Absolutely beautiful! The craftsmanship is outstanding.',
        date: '2 weeks ago'
      },
      {
        id: 2,
        user: 'Jane Smith',
        rating: 4,
        comment: 'Great quality, shipping was fast. Very happy with my purchase.',
        date: '1 month ago'
      },
      {
        id: 3,
        user: 'Mike Wilson',
        rating: 5,
        comment: 'Perfect gift! The recipient loved it.',
        date: '1 month ago'
      }
    ]
  }

  const handleAddToCart = () => {
    alert(`Added ${quantity} ${product.title} to cart!`)
    navigate('/cart')
  }

  const handleBuyNow = () => {
    navigate('/checkout')
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />
      
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Back Button */}
          <Link to="/explore" className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-6">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Explore
          </Link>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-12">
            {/* Product Images */}
            <div>
              <div className="bg-white rounded-2xl overflow-hidden shadow-sm mb-4">
                <img 
                  src={product.images[activeImage]} 
                  alt={product.title}
                  className="w-full h-[300px] sm:h-[400px] lg:h-[500px] object-cover"
                />
              </div>
              <div className="grid grid-cols-3 gap-4">
                {product.images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setActiveImage(index)}
                    className={`rounded-lg overflow-hidden border-2 transition-all ${
                      activeImage === index ? 'border-primary' : 'border-transparent'
                    }`}
                  >
                    <img 
                      src={image} 
                      alt={`${product.title} ${index + 1}`}
                      className="w-full h-24 object-cover"
                    />
                  </button>
                ))}
              </div>
            </div>

            {/* Product Info */}
            <div>
              <div className="bg-white rounded-2xl shadow-sm p-8">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <span className="text-sm text-gray-600">{product.category} / {product.subcategory}</span>
                    <h1 className="text-3xl font-bold text-gray-900 mt-2">
                      {product.title}
                    </h1>
                  </div>
                  <button className="p-2 text-gray-400 hover:text-red-500 transition-colors">
                    <Heart className="w-6 h-6" />
                  </button>
                </div>

                <div className="flex items-center space-x-4 mb-6 pb-6 border-b border-gray-200">
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`w-5 h-5 ${i < Math.floor(product.artisan.rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
                      />
                    ))}
                  </div>
                  <span className="text-gray-600">
                    {product.artisan.rating} ({product.artisan.totalReviews} reviews)
                  </span>
                </div>

                <div className="mb-6">
                  <span className="text-4xl font-bold text-gray-900">
                    KSH {product.price.toFixed(2)}
                  </span>
                  <span className={`ml-4 text-sm font-medium ${product.inStock ? 'text-green-600' : 'text-red-600'}`}>
                    {product.inStock ? 'In Stock' : 'Out of Stock'}
                  </span>
                </div>

                <p className="text-gray-700 mb-6 leading-relaxed">
                  {product.description}
                </p>

                {/* Artisan Info */}
                <Link to={`/artisan/${product.artisan.id}`} className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg mb-6 hover:bg-gray-100 transition-colors">
                  <img 
                    src={product.artisan.avatar} 
                    alt={product.artisan.name}
                    className="w-12 h-12 rounded-full object-cover"
                  />
                  <div>
                    <p className="text-sm text-gray-600">Artisan</p>
                    <p className="font-bold text-gray-900">{product.artisan.name}</p>
                  </div>
                </Link>

                {/* Quantity Selector */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quantity
                  </label>
                  <div className="flex items-center space-x-4">
                    <button
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      className="w-10 h-10 rounded-lg border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                    >
                      -
                    </button>
                    <span className="text-lg font-medium w-12 text-center">{quantity}</span>
                    <button
                      onClick={() => setQuantity(quantity + 1)}
                      className="w-10 h-10 rounded-lg border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                    >
                      +
                    </button>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="space-y-3">
                  <button
                    onClick={handleBuyNow}
                    disabled={!product.inStock}
                    className="w-full btn-primary py-3 text-base sm:text-lg disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Buy Now
                  </button>
                  <button
                    onClick={handleAddToCart}
                    disabled={!product.inStock}
                    className="w-full btn-secondary py-3 text-base sm:text-lg flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <ShoppingCart className="w-5 h-5" />
                    <span>Add to Cart</span>
                  </button>
                  <Link
                    to={`/messages/${product.artisan.id}`}
                    className="w-full btn-secondary py-3 text-base sm:text-lg flex items-center justify-center space-x-2"
                  >
                    <MessageSquare className="w-5 h-5" />
                    <span>Message Artisan</span>
                  </Link>
                </div>
              </div>
            </div>
          </div>

          {/* Reviews Section */}
          <div className="mt-12">
            <div className="bg-white rounded-2xl shadow-sm p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Customer Reviews ({product.reviews.length})
              </h2>
              
              <div className="space-y-6">
                {product.reviews.map((review) => (
                  <div key={review.id} className="border-b border-gray-200 pb-6 last:border-0">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
                          <User className="w-5 h-5 text-gray-600" />
                        </div>
                        <div>
                          <p className="font-bold text-gray-900">{review.user}</p>
                          <div className="flex items-center space-x-2">
                            <div className="flex">
                              {[...Array(5)].map((_, i) => (
                                <Star 
                                  key={i} 
                                  className={`w-4 h-4 ${i < review.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
                                />
                              ))}
                            </div>
                            <span className="text-sm text-gray-500">{review.date}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <p className="text-gray-700 ml-13">{review.comment}</p>
                  </div>
                ))}
              </div>

              <button className="mt-6 text-primary hover:text-primary-hover font-medium">
                Write a Review
              </button>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default ProductDetailPage
