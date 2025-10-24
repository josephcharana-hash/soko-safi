import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Diamond } from 'lucide-react'

const RegisterPage = () => {
  const navigate = useNavigate()
  const [userType, setUserType] = useState('artisan')
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: ''
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Register:', { ...formData, userType })
    if (userType === 'artisan') {
      navigate('/artisan-dashboard')
    } else {
      navigate('/buyer-dashboard')
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <Diamond className="w-6 h-6 text-primary-600" fill="currentColor" />
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
            
            <Link to="/login" className="btn-primary px-6 py-2">
              Log In
            </Link>
          </div>
        </div>
      </nav>

      <div className="flex items-center justify-center px-4 py-12">
        <div className="max-w-md w-full">
          <div className="bg-white rounded-2xl shadow-sm p-8">
            <div className="text-center mb-8">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Create your account
              </h1>
              <p className="text-gray-600">
                Join our community of artisans and buyers.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  I am a...
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setUserType('artisan')}
                    className={`py-2.5 px-4 rounded-lg font-medium transition-all duration-200 ${
                      userType === 'artisan'
                        ? 'bg-primary-600 text-white'
                        : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    Artisan
                  </button>
                  <button
                    type="button"
                    onClick={() => setUserType('buyer')}
                    className={`py-2.5 px-4 rounded-lg font-medium transition-all duration-200 ${
                      userType === 'buyer'
                        ? 'bg-primary-600 text-white'
                        : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    Buyer
                  </button>
                </div>
              </div>

              <div>
                <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  id="fullName"
                  name="fullName"
                  value={formData.fullName}
                  onChange={handleChange}
                  placeholder="Enter your full name"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Enter your email"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  className="input-field"
                  required
                />
              </div>

              <button
                type="submit"
                className="w-full btn-primary py-3"
              >
                Sign up
              </button>

              <p className="text-center text-sm text-gray-600">
                Already have an account?{' '}
                <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
                  Log in
                </Link>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RegisterPage
