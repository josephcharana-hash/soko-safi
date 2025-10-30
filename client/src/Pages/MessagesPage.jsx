import { useState, useEffect } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { Diamond, Send, User, ArrowLeft, Paperclip, Image as ImageIcon, Loader } from 'lucide-react'
import { api } from '../services/api'

const MessagesPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [messageText, setMessageText] = useState('')
  const [selectedConversation, setSelectedConversation] = useState(id ? parseInt(id) : null)
  const [conversations, setConversations] = useState([])
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadConversations()
  }, [])

  useEffect(() => {
    if (selectedConversation) {
      loadMessages(selectedConversation)
    }
  }, [selectedConversation])

  const loadConversations = async () => {
    try {
      setLoading(true)
      const data = await api.messages.getConversations()
      setConversations(Array.isArray(data) ? data : [])
      
      if (!data || data.length === 0) {
        setSelectedConversation(null)
      } else if (!selectedConversation) {
        setSelectedConversation(data[0].id)
      }
    } catch (error) {
      console.error('Failed to load conversations:', error)
      setError('Failed to load conversations')
      setConversations(mockConversations)
      if (!selectedConversation && mockConversations.length > 0) {
        setSelectedConversation(mockConversations[0].id)
      }
    } finally {
      setLoading(false)
    }
  }

  const loadMessages = async (conversationId) => {
    try {
      const data = await api.messages.getMessages(conversationId)
      setMessages(Array.isArray(data) ? data : [])
    } catch (error) {
      console.error('Failed to load messages:', error)
      const mockConv = mockConversations.find(c => c.id === conversationId)
      setMessages(mockConv ? mockConv.messages : [])
    }
  }

  const mockConversations = [
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
    }
  ]

  const currentConversation = conversations.find(c => c.id === selectedConversation)

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!messageText.trim() || !currentConversation) return
    
    try {
      setSending(true)
      const receiverId = currentConversation.artisan?.id || currentConversation.user_id
      await api.messages.send(receiverId, messageText.trim())
      
      const newMessage = {
        id: Date.now(),
        sender: 'buyer',
        text: messageText.trim(),
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
      setMessages(prev => [...prev, newMessage])
      setMessageText('')
      
      setTimeout(() => loadMessages(selectedConversation), 1000)
    } catch (error) {
      console.error('Failed to send message:', error)
      alert('Failed to send message. Please try again.')
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
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
            <div className="w-full md:w-80 border-b md:border-b-0 md:border-r border-gray-200 flex flex-col max-h-48 md:max-h-none">
              <div className="p-4 border-b border-gray-200">
                <h2 className="text-xl font-bold text-gray-900">Messages</h2>
              </div>
              
              <div className="flex-1 overflow-y-auto hidden md:block">
                {loading ? (
                  <div className="p-4 text-center">
                    <Loader className="w-6 h-6 text-primary mx-auto mb-2 animate-spin" />
                    <p className="text-sm text-gray-600">Loading conversations...</p>
                  </div>
                ) : conversations.length === 0 ? (
                  <div className="p-4 text-center">
                    <p className="text-gray-600">No conversations yet</p>
                    <Link to="/explore" className="text-primary hover:text-primary-700 text-sm">
                      Browse products to start chatting with artisans
                    </Link>
                  </div>
                ) : (
                  conversations.map((conversation) => (
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
                  ))
                )}
              </div>
            </div>

            {currentConversation ? (
              <div className="flex-1 flex flex-col">
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

                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                  {messages.map((message) => (
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
                      disabled={!messageText.trim() || sending}
                      className="btn-primary p-3 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {sending ? (
                        <Loader className="w-5 h-5 animate-spin" />
                      ) : (
                        <Send className="w-5 h-5" />
                      )}
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