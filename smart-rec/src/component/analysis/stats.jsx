import React from 'react';
import { Users, Clock, UserX } from 'lucide-react';
import type { DashboardStats } from '../types';

interface StatsProps {
  stats: DashboardStats;
}

export function DashboardStats({ stats }: StatsProps) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <div className="bg-green-50 rounded-lg p-6 shadow">
        <div className="flex items-center">
          <Users className="h-8 w-8 text-green-600" />
          <div className="ml-4">
            <p className="text-sm font-medium text-green-600">Present Today</p>
            <p className="text-2xl font-semibold text-green-900">{stats.present}</p>
          </div>
        </div>
      </div>

      <div className="bg-yellow-50 rounded-lg p-6 shadow">
        <div className="flex items-center">
          <Clock className="h-8 w-8 text-yellow-600" />
          <div className="ml-4">
            <p className="text-sm font-medium text-yellow-600">Late</p>
            <p className="text-2xl font-semibold text-yellow-900">{stats.late}</p>
          </div>
        </div>
      </div>

      <div className="bg-red-50 rounded-lg p-6 shadow">
        <div className="flex items-center">
          <UserX className="h-8 w-8 text-red-600" />
          <div className="ml-4">
            <p className="text-sm font-medium text-red-600">Absent</p>
            <p className="text-2xl font-semibold text-red-900">{stats.absent}</p>
          </div>
        </div>
      </div>
    </div>
  );
}