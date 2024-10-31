import React from 'react';
import { Menu, Bell, User } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <button className="p-2 rounded-md text-gray-400 hover:text-gray-500 lg:hidden">
              <Menu className="h-6 w-6" />
            </button>
            <div className="hidden lg:flex lg:items-center lg:space-x-4">
              <h1 className="text-2xl font-bold text-gray-900">SmartAttend</h1>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <button className="p-2 rounded-full text-gray-400 hover:text-gray-500">
              <Bell className="h-6 w-6" />
            </button>
            <button className="p-2 rounded-full text-gray-400 hover:text-gray-500">
              <User className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}