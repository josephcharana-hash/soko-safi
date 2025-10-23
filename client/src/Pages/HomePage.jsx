import { Link } from 'react-router-dom'
import Navbar from '../Components/Layout/Navbar'
import Footer from '../Components/Layout/Footer'

const HomePage = () => {
  const featuredWorks = [
    {
      id: 1,
      title: 'Ceramic Vase',
      description: 'Handcrafted ceramic vase with a unique glaze.',
      image: '/images/ceramic-vase.jpg'
    },
    {
      id: 2,
      title: 'Woven Basket',
      description: 'Woven basket with intricate patterns and natural dyes.',
      image: '/images/woven-basket.jpg'
    },
    {
      id: 3,
      title: 'Wood Carving',
      description: 'Detailed wood carving of a native animal.',
      image: '/images/wood-carving.jpg'
    },
    {
      id: 4,
      title: 'Textile Art',
      description: 'Colorful textile art piece depicting a local scene.',
      image: '/images/textile-art.jpg'
    }
  ]

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      {/* Hero Section */}
      <section 
        className="relative h-[500px] flex items-center justify-center text-white"
        style={{
          backgroundImage: 'url(/images/hero-bg.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      >
        <div className="absolute inset-0 bg-black/50"></div>
        <div className="relative z-10 text-center px-4 max-w-3xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            Discover Local Artisans
          </h1>
          <p className="text-lg md:text-xl mb-8 text-gray-100">
            Explore unique, handcrafted goods from talented artisans in your community.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register" className="btn-primary text-base px-8 py-3">
              Sign Up as Artisan
            </Link>
            <Link to="/explore" className="btn-secondary text-base px-8 py-3">
              Explore Works
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Works Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-900 mb-12">
          Featured Works
        </h2>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {featuredWorks.map((work) => (
            <Link key={work.id} to="/explore" className="card group cursor-pointer hover:shadow-lg transition-shadow duration-300">
              <div className="aspect-square overflow-hidden">
                <img
                  src={work.image}
                  alt={work.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div className="p-5">
                <h3 className="text-lg font-bold text-gray-900 mb-2">
                  {work.title}
                </h3>
                <p className="text-sm text-gray-600">
                  {work.description}
                </p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <Footer />
    </div>
  )
}

export default HomePage
