import React from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

function BuyerDashboard() {
  const [activeTab, setActiveTab] = useState("orders");

  // Mock data
  const orders = [
    {
      id: "#1234",
      product: "Ceramic Vase",
      artisan: "Sarah Johnson",
      price: 45.0,
      status: "Delivered",
      date: "2025-10-10",
      image:
        "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=100&h=100&fit=crop",
      canReview: true,
    },
    {
      id: "#1233",
      product: "Wood Carving",
      artisan: "John Smith",
      price: 120.0,
      status: "In Transit",
      date: "2025-10-14",
      image:
        "https://images.unsplash.com/photo-1551522435-a13afa10f103?w=100&h=100&fit=crop",
      canReview: false,
    },
    {
      id: "#1232",
      product: "Textile Art",
      artisan: "Maria Garcia",
      price: 85.0,
      status: "Processing",
      date: "2025-10-15",
      image:
        "https://images.unsplash.com/photo-1558769132-cb1aea3c8565?w=100&h=100&fit=crop",
      canReview: false,
    },
  ];

  const messages = [
    {
      id: 1,
      artisan: "Sarah Johnson",
      lastMessage:
        "Thank you for your purchase! Let me know if you need anything.",
      time: "2 hours ago",
      unread: true,
    },
    {
      id: 2,
      artisan: "John Smith",
      lastMessage: "Your order has been shipped!",
      time: "1 day ago",
      unread: false,
    },
    {
      id: 3,
      artisan: "Maria Garcia",
      lastMessage: "I can customize that piece for you.",
      time: "3 days ago",
      unread: false,
    },
  ];

  const collections = [
    {
      id: 1,
      name: "Favorites",
      itemCount: 12,
      image:
        "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=200&h=200&fit=crop",
    },
    {
      id: 2,
      name: "Wishlist",
      itemCount: 8,
      image:
        "https://images.unsplash.com/photo-1551522435-a13afa10f103?w=200&h=200&fit=crop",
    },
    {
      id: 3,
      name: "Gift Ideas",
      itemCount: 5,
      image:
        "https://images.unsplash.com/photo-1558769132-cb1aea3c8565?w=200&h=200&fit=crop",
    },
  ];

  const paymentHistory = [
    {
      id: 1,
      orderId: "#1234",
      amount: 45.0,
      date: "2025-10-10",
      method: "Credit Card",
      status: "Completed",
    },
    {
      id: 2,
      orderId: "#1233",
      amount: 120.0,
      date: "2025-10-14",
      method: "PayPal",
      status: "Completed",
    },
    {
      id: 3,
      orderId: "#1232",
      amount: 85.0,
      date: "2025-10-15",
      method: "Credit Card",
      status: "Pending",
    },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case "Delivered":
      case "Completed":
        return "bg-green-100 text-green-800";
      case "In Transit":
        return "bg-blue-100 text-blue-800";
      case "Processing":
      case "Pending":
        return "bg-yellow-100 text-yellow-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return <div>BuyerDashboard</div>;
}

export default BuyerDashboard;
