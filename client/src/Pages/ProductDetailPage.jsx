import { useState, useEffect } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import {
  ShoppingCart,
  Heart,
  Star,
  MessageSquare,
  ArrowLeft,
  User,
  Truck,
  Shield,
  RotateCcw,
  MapPin,
  Clock,
  CheckCircle,
  Share2,
  Plus,
  Minus,
  Eye,
} from "lucide-react";
import Navbar from "../Components/Layout/Navbar";
import Footer from "../Components/Layout/Footer";
import LazyImage from "../Components/LazyImage";
import LoadingSpinner from "../Components/LoadingSpinner";
import ReviewModal from "../Components/ReviewModal";
import { api } from "../services/api";

const ProductDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [quantity, setQuantity] = useState(1);
  const [activeImage, setActiveImage] = useState(0);
  const [selectedSize, setSelectedSize] = useState("");
  const [isWishlisted, setIsWishlisted] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch product
  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const productData = await api.products.getById(id);
        setProduct(productData);
      } catch (error) {
        console.error("Failed to fetch product:", error);
        setError("Product not found");
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Navbar />
        <div className="flex-1 flex items-center justify-center pt-20">
          <LoadingSpinner size="lg" text="Loading product..." />
        </div>
        <Footer />
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Navbar />
        <div className="flex-1 flex items-center justify-center pt-20">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Product Not Found
            </h2>
            <p className="text-gray-600 mb-6">
              The product you're looking for doesn't exist.
            </p>
            <Link to="/explore" className="btn-primary">
              Browse Products
            </Link>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  // Fill missing product data
  const productWithDefaults = {
    ...product,
    images:
      product.images && product.images.length
        ? product.images
        : ["/images/placeholder.svg"],
    category: product.category || "Handcraft",
    subcategory: product.subcategory || "Art",
    inStock: product.stock > 0,
    stockCount: product.stock || 0,
    artisan: {
      id: product.artisan_id || 1,
      name: product.artisan_name || "Master Artisan",
      avatar: "/images/placeholder.svg",
      rating: 4.5,
      totalReviews: 12,
      location: "Kenya",
      responseTime: "< 24 hours",
    },
    shipping: {
      cost: 300,
      time: "3-5 business days",
      freeThreshold: 5000,
    },
    reviews: product.reviews || [],
  };

  // Handlers
  const handleAddToCart = async () => {
    try {
      await api.cart.add(product.id, quantity);
      alert(`Added ${quantity} ${product.title} to cart!`);
    } catch (error) {
      console.error("Failed to add to cart:", error);
      alert("Failed to add item to cart. Please try again.");
    }
  };

  const handleBuyNow = async () => {
    try {
      await api.cart.add(product.id, quantity);
      navigate("/checkout");
    } catch (error) {
      console.error("Failed to buy now:", error);
      alert("Failed to buy item. Please try again.");
    }
  };

  const handleWishlistToggle = async () => {
    try {
      if (isWishlisted) await api.favorites.remove(product.id);
      else await api.favorites.add(product.id);
      setIsWishlisted(!isWishlisted);
    } catch (error) {
      alert("Failed to update wishlist. Please try again.");
    }
  };

  const handleWriteReview = () => setShowReviewModal(true);

  const handleReviewSubmit = async (reviewData) => {
    try {
      await api.reviews.create({
        product_id: product.id,
        rating: reviewData.rating,
        comment: reviewData.review,
      });
      alert("Review submitted successfully!");
      setShowReviewModal(false);
    } catch {
      alert("Failed to submit review. Please try again.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />
      <main className="flex-1 pt-20">
        <div className="max-w-7xl mx-auto px-4 py-8">
          {/* Breadcrumb */}
          <nav className="flex items-center space-x-2 text-sm text-gray-500 mb-6">
            <Link to="/" className="hover:text-primary-600">
              Home
            </Link>
            <span>/</span>
            <Link to="/explore" className="hover:text-primary-600">
              Explore
            </Link>
            <span>/</span>
            <span className="text-gray-900">{product.title}</span>
          </nav>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Images */}
            <div>
              <div className="bg-white rounded-2xl overflow-hidden shadow-sm mb-4">
                <LazyImage
                  src={productWithDefaults.images[activeImage]}
                  alt={product.title}
                  className="w-full h-[500px] object-cover"
                />
              </div>

              <div className="grid grid-cols-3 gap-4">
                {productWithDefaults.images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setActiveImage(index)}
                    className={`rounded-lg overflow-hidden border-2 ${
                      activeImage === index
                        ? "border-primary-500"
                        : "border-transparent"
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

            {/* Info */}
            <div className="space-y-6">
              <div className="bg-white rounded-2xl shadow-sm p-8">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <span className="text-sm text-gray-600">
                      {productWithDefaults.category} /{" "}
                      {productWithDefaults.subcategory}
                    </span>
                    <h1 className="text-3xl font-bold text-gray-900 mt-2">
                      {product.title}
                    </h1>
                    <div className="flex items-center mt-2 space-x-2">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`w-5 h-5 ${
                            i <
                            Math.floor(productWithDefaults.artisan.rating)
                              ? "text-yellow-400"
                              : "text-gray-300"
                          }`}
                        />
                      ))}
                      <span className="text-gray-600">
                        ({productWithDefaults.artisan.totalReviews} reviews)
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={handleWishlistToggle}
                    className={`p-3 rounded-full ${
                      isWishlisted
                        ? "bg-red-100 text-red-500"
                        : "bg-gray-100 text-gray-400"
                    }`}
                  >
                    <Heart
                      className={`w-6 h-6 ${
                        isWishlisted ? "fill-current" : ""
                      }`}
                    />
                  </button>
                </div>

                <div className="text-4xl font-bold text-gray-900 mb-4">
                  KSh {product.price?.toLocaleString()}
                </div>

                <div className="flex items-center mb-6">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                  <span
                    className={`font-medium ${
                      productWithDefaults.inStock
                        ? "text-green-600"
                        : "text-red-600"
                    }`}
                  >
                    {productWithDefaults.inStock
                      ? "In Stock"
                      : "Out of Stock"}
                  </span>
                </div>

                {/* Quantity */}
                <div className="flex items-center space-x-4 mb-6">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="p-2 border rounded-lg"
                  >
                    <Minus />
                  </button>
                  <span className="text-lg font-semibold">{quantity}</span>
                  <button
                    onClick={() => setQuantity(quantity + 1)}
                    className="p-2 border rounded-lg"
                  >
                    <Plus />
                  </button>
                </div>

                {/* Actions */}
                <div className="space-y-3">
                  <button
                    onClick={handleBuyNow}
                    className="w-full bg-primary-600 text-white py-3 rounded-lg hover:bg-primary-700"
                  >
                    Buy Now • KSh{" "}
                    {(product.price * quantity).toLocaleString()}
                  </button>
                  <button
                    onClick={handleAddToCart}
                    className="w-full bg-gray-100 text-gray-900 py-3 rounded-lg hover:bg-gray-200 flex justify-center items-center space-x-2"
                  >
                    <ShoppingCart className="w-5 h-5" />
                    <span>Add to Cart</span>
                  </button>
                </div>
              </div>

              {/* Artisan Info */}
              <div className="bg-white p-6 rounded-2xl shadow-sm">
                <h3 className="font-semibold text-lg mb-4">
                  Meet the Artisan
                </h3>
                <Link
                  to={`/artisan/${productWithDefaults.artisan.id}`}
                  className="flex items-center space-x-4"
                >
                  <img
                    src={productWithDefaults.artisan.avatar}
                    alt={productWithDefaults.artisan.name}
                    className="w-16 h-16 rounded-full object-cover"
                  />
                  <div>
                    <h4 className="font-semibold text-gray-900">
                      {productWithDefaults.artisan.name}
                    </h4>
                    <p className="text-gray-600">
                      {productWithDefaults.artisan.location}
                    </p>
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
      {showReviewModal && (
        <ReviewModal
          onClose={() => setShowReviewModal(false)}
          onSubmit={handleReviewSubmit}
        />
      )}
    </div>
  );
};

export default ProductDetailPage;

