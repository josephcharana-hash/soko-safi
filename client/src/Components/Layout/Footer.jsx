import { Link } from 'react-router-dom'
import { Diamond } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col items-center space-y-6">
          <Link to="/" className="flex items-center space-x-2">
            <Diamond className="w-6 h-6 text-primary" fill="currentColor" />
            <span className="text-xl font-bold text-gray-900">SokoDigital</span>
          </Link>
          
          <div className="flex items-center space-x-8 text-sm">
            <Link to="/about" className="text-gray-600 hover:text-gray-900">
              About
            </Link>
            <Link to="/contact" className="text-gray-600 hover:text-gray-900">
              Contact
            </Link>
            <Link to="/terms" className="text-gray-600 hover:text-gray-900">
              Terms of Service
            </Link>
            <Link to="/privacy" className="text-gray-600 hover:text-gray-900">
              Privacy Policy
            </Link>
          </div>
          
          <p className="text-sm text-gray-500">
            © 2024 SokoDigital. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer

