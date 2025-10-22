import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Diamond, ShoppingCart, MessageSquare, User, Menu, X } from 'lucide-react'

const Navbar = ({ showAuthButtons = true, isLoggedIn = false }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Diamond className="w-6 h-6 text-primary" fill="currentColor" />
            <span className="text-xl font-bold text-gray-900">SokoDigital</span>
          </Link>
          
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-gray-900 font-medium">
              Home
            </Link>
            <Link to="/explore" className="text-gray-700 hover:text-gray-900 font-medium">
              Explore
            </Link>
            <Link to="/about" className="text-gray-700 hover:text-gray-900 font-medium">
              About
            </Link>
          </div>
          
          <div className="flex items-center space-x-2">
            {/* Desktop Auth Buttons */}
            {showAuthButtons && !isLoggedIn && (
              <div className="hidden md:flex items-center space-x-4">
                <Link to="/login" className="text-gray-700 hover:text-gray-900 font-medium">
                  Log In
                </Link>
                <Link to="/register" className="btn-primary">
                  Sign Up
                </Link>
              </div>
            )}

            {/* Desktop User Menu */}
            {isLoggedIn && (
              <div className="hidden md:flex items-center space-x-4">
                <Link to="/messages" className="p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100 relative">
                  <MessageSquare className="w-5 h-5" />
                  <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                </Link>
                <Link to="/cart" className="p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100 relative">
                  <ShoppingCart className="w-5 h-5" />
                  <span className="absolute -top-1 -right-1 w-5 h-5 bg-primary text-white text-xs rounded-full flex items-center justify-center">
                    3
                  </span>
                </Link>
                <Link to="/buyer-dashboard" className="flex items-center space-x-2 p-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-white" />
                  </div>
                </Link>
              </div>
            )}

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 text-gray-600 hover:text-gray-900"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200">
            <div className="flex flex-col space-y-3">
              <Link 
                to="/" 
                className="text-gray-700 hover:text-gray-900 font-medium px-2 py-2 rounded-lg hover:bg-gray-50"
                onClick={() => setMobileMenuOpen(false)}
              >
                Home
              </Link>
              <Link 
                to="/explore" 
                className="text-gray-700 hover:text-gray-900 font-medium px-2 py-2 rounded-lg hover:bg-gray-50"
                onClick={() => setMobileMenuOpen(false)}
              >
                Explore
              </Link>
              <Link 
                to="/about" 
                className="text-gray-700 hover:text-gray-900 font-medium px-2 py-2 rounded-lg hover:bg-gray-50"
                onClick={() => setMobileMenuOpen(false)}
              >
                About
              </Link>
              {showAuthButtons && !isLoggedIn && (
                <>
                  <Link 
                    to="/login" 
                    className="text-gray-700 hover:text-gray-900 font-medium px-2 py-2 rounded-lg hover:bg-gray-50"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Log In
                  </Link>
                  <Link 
                    to="/register" 
                    className="btn-primary text-center"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Sign Up
                  </Link>
                </>
              )}
              {isLoggedIn && (
                <>
                  <Link 
                    to="/cart" 
                    className="text-gray-700 hover:text-gray-900 font-medium px-2 py-2 rounded-lg hover:bg-gray-50 flex items-center justify-between"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <span>Cart</span>
                    <span className="bg-primary text-white text-xs px-2 py-1 rounded-full">3</span>
                  </Link>
                  <Link 
                    to="/messages" 
                    className="text-gray-700 hover:text-gray-900 font-medium px-2 py-2 rounded-lg hover:bg-gray-50 flex items-center justify-between"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <span>Messages</span>
                    <span className="w-2 h-2 bg-red-500 rounded-full"></span>
                  </Link>
                  <Link 
                    to="/buyer-dashboard" 
                    className="text-gray-700 hover:text-gray-900 font-medium px-2 py-2 rounded-lg hover:bg-gray-50"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Dashboard
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
