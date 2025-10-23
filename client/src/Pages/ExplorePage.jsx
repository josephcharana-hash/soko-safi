import { Link } from 'react-router-dom'
import Navbar from '../Components/Layout/Navbar'
import Footer from '../Components/Layout/Footer'

const ExplorePage = () => {
  const works = [
    {
      id: 1,
      title: 'Ceramic Vase',
      description: 'Handcrafted ceramic vase with a unique glaze.',
      price: 45.00,
      image: '/images/ceramic-vase.jpg'
    },
    {
      id: 2,
      title: 'Woven Basket',
      description: 'Woven basket with intricate patterns and natural dyes.',
      price: 32.00,
      image: '/images/woven-basket.jpg'
    },
    {
      id: 3,
      title: 'Wood Carving',
      description: 'Detailed wood carving of a native animal.',
      price: 120.00,
      image: '/images/wood-carving.jpg'
    },
    {
      id: 4,
      title: 'Textile Art',
      description: 'Colorful textile art piece depicting a local scene.',
      price: 85.00,
      image: '/images/textile-art.jpg'
    },
    {
      id: 5,
      title: 'Pottery Bowl',
      description: 'Beautiful handmade pottery bowl.',
      price: 38.00,
      image: '/images/pottery-bowl.jpg'
    },
    {
      id: 6,
      title: 'Macrame Wall Hanging',
      description: 'Intricate macrame wall decoration.',
      price: 65.00,
      image: '/images/macrame-wall-hanging.jpg'
    }
  ]

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
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
              <Link key={work.id} to={`/product/${work.id}`} className="card group cursor-pointer hover:shadow-lg transition-shadow duration-300">
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
                  <p className="text-sm text-gray-600 mb-3">
                    {work.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-xl font-bold text-gray-900">
                      KSH {work.price.toFixed(2)}
                    </span>
                    <span className="btn-primary text-sm px-4 py-2">
                      View Details
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default ExplorePage
