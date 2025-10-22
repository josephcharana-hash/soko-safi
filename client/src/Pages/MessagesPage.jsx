import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { Diamond, Send, User, ArrowLeft, Paperclip, Image as ImageIcon } from 'lucide-react'

const MessagesPage = () => {
  const { id } = useParams()
  const [messageText, setMessageText] = useState('')
  const [selectedConversation, setSelectedConversation] = useState(id ? parseInt(id) : 1)

  // Mock conversations data
  const conversations = [
    {
      id: 1,
      artisan: {
        id: 1,
        name: 'Sarah Johnson',
        avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop',
        online: true
      },
      lastMessage: 'Thank you for your purchase!',
      lastMessageTime: '2 hours ago',
      unread: 2,
      messages: [
        {
          id: 1,
          sender: 'artisan',
          text: 'Hi! Thank you for your interest in my ceramic vase.',
          time: '10:30 AM'
        },
        {
          id: 2,
          sender: 'buyer',
          text: 'Hello! Can you tell me more about the glaze used?',
          time: '10:35 AM'
        },
        {
          id: 3,
          sender: 'artisan',
          text: 'Of course! I use a food-safe glaze that I mix myself. It creates that unique blue-green color you see in the photos.',
          time: '10:40 AM'
        },
        {
          id: 4,
          sender: 'buyer',
          text: 'That sounds perfect! I\'ll take it.',
          time: '10:45 AM'
        },
        {
          id: 5,
          sender: 'artisan',
          text: 'Thank you for your purchase! I\'ll ship it out tomorrow.',
          time: '11:00 AM'
        }
      ]
    },
    {
      id: 2,
      artisan: {
        id: 2,
        name: 'John Smith',
        avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop',
        online: false
      },
      lastMessage: 'Your order has been shipped!',
      lastMessageTime: '1 day ago',
      unread: 0,
      messages: [
        {
          id: 1,
          sender: 'buyer',
          text: 'Hi! When will my order ship?',
          time: 'Yesterday 3:00 PM'
        },
        {
          id: 2,
          sender: 'artisan',
          text: 'Your order has been shipped! Tracking number: 1Z999AA10123456784',
          time: 'Yesterday 4:30 PM'
        }
      ]
    },
    {
      id: 3,
      artisan: {
        id: 3,
        name: 'Maria Garcia',
        avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop',
        online: true
      },
      lastMessage: 'I can customize that for you.',
      lastMessageTime: '3 days ago',
      unread: 0,
      messages: [
        {
          id: 1,
          sender: 'buyer',
          text: 'Can you make this in a different color?',
          time: '3 days ago'
        },
        {
          id: 2,
          sender: 'artisan',
          text: 'I can customize that for you. What color did you have in mind?',
          time: '3 days ago'
        }
      ]
    }
  ]

  const currentConversation = conversations.find(c => c.id === selectedConversation)

  const handleSendMessage = (e) => {
    e.preventDefault()
    if (messageText.trim()) {
      console.log('Sending message:', messageText)
      // Add message logic here
      setMessageText('')
    }
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
            
            <Link to="/buyer-dashboard" className="text-gray-600 hover:text-gray-900 font-medium">
              Back to Dashboard
            </Link>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-2xl shadow-sm overflow-hidden h-[600px] md:h-[calc(100vh-200px)]">
          <div className="flex h-full flex-col md:flex-row">
            {/* Conversations List */}
            <div className="w-full md:w-80 border-b md:border-b-0 md:border-r border-gray-200 flex flex-col max-h-48 md:max-h-none">
              <div className="p-4 border-b border-gray-200">
                <h2 className="text-xl font-bold text-gray-900">Messages</h2>
              </div>
              
              <div className="flex-1 overflow-y-auto hidden md:block">
                {conversations.map((conversation) => (
                  <button
                    key={conversation.id}
                    onClick={() => setSelectedConversation(conversation.id)}
                    className={`w-full p-3 md:p-4 flex items-start space-x-3 hover:bg-gray-50 transition-colors border-b border-gray-100 ${
                      selectedConversation === conversation.id ? 'bg-primary/5' : ''
                    }`}
                  >
                    <div className="relative">
                      <img 
                        src={conversation.artisan.avatar} 
                        alt={conversation.artisan.name}
                        className="w-12 h-12 rounded-full object-cover"
                      />
                      {conversation.artisan.online && (
                        <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
                      )}
                    </div>
                    <div className="flex-1 text-left">
                      <div className="flex items-center justify-between mb-1">
                        <p className="font-bold text-gray-900">{conversation.artisan.name}</p>
                        {conversation.unread > 0 && (
                          <span className="w-5 h-5 bg-primary text-white text-xs rounded-full flex items-center justify-center">
                            {conversation.unread}
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600 truncate">{conversation.lastMessage}</p>
                      <p className="text-xs text-gray-500 mt-1">{conversation.lastMessageTime}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Chat Area */}
            {currentConversation ? (
              <div className="flex-1 flex flex-col">
                {/* Chat Header */}
                <div className="p-4 border-b border-gray-200 flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <img 
                      src={currentConversation.artisan.avatar} 
                      alt={currentConversation.artisan.name}
                      className="w-10 h-10 rounded-full object-cover"
                    />
                    <div>
                      <Link 
                        to={`/artisan/${currentConversation.artisan.id}`}
                        className="font-bold text-gray-900 hover:text-primary"
                      >
                        {currentConversation.artisan.name}
                      </Link>
                      <p className="text-sm text-gray-600">
                        {currentConversation.artisan.online ? 'Online' : 'Offline'}
                      </p>
                    </div>
                  </div>
                  <Link 
                    to={`/artisan/${currentConversation.artisan.id}`}
                    className="btn-secondary text-sm px-4 py-2"
                  >
                    View Profile
                  </Link>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                  {currentConversation.messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.sender === 'buyer' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`max-w-md ${message.sender === 'buyer' ? 'order-2' : 'order-1'}`}>
                        <div
                          className={`rounded-2xl px-4 py-3 ${
                            message.sender === 'buyer'
                              ? 'bg-primary text-white'
                              : 'bg-gray-100 text-gray-900'
                          }`}
                        >
                          <p>{message.text}</p>
                        </div>
                        <p className={`text-xs text-gray-500 mt-1 ${message.sender === 'buyer' ? 'text-right' : 'text-left'}`}>
                          {message.time}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Message Input */}
                <div className="p-4 border-t border-gray-200">
                  <form onSubmit={handleSendMessage} className="flex items-end space-x-3">
                    <div className="flex space-x-2">
                      <button
                        type="button"
                        className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                        title="Attach file"
                      >
                        <Paperclip className="w-5 h-5" />
                      </button>
                      <button
                        type="button"
                        className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                        title="Attach image"
                      >
                        <ImageIcon className="w-5 h-5" />
                      </button>
                    </div>
                    <div className="flex-1">
                      <textarea
                        value={messageText}
                        onChange={(e) => setMessageText(e.target.value)}
                        placeholder="Type your message..."
                        rows="3"
                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault()
                            handleSendMessage(e)
                          }
                        }}
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={!messageText.trim()}
                      className="btn-primary p-3 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <Send className="w-5 h-5" />
                    </button>
                  </form>
                  <p className="text-xs text-gray-500 mt-2">Press Enter to send, Shift+Enter for new line</p>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex items-center justify-center text-gray-500">
                <p>Select a conversation to start messaging</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default MessagesPage
