'use client';

import React from 'react';
import { Tag } from 'lucide-react';

interface EntityDisplayProps {
  entities: { [key: string]: string[] };
}

export default function EntityDisplay({ entities }: EntityDisplayProps) {
  if (!entities || Object.keys(entities).length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Tag className="text-blue-500" size={24} />
          Named Entities
        </h3>
        <p className="text-gray-500 text-center py-4">No entities detected</p>
      </div>
    );
  }

  const getColorForType = (type: string) => {
    const colors: { [key: string]: string } = {
      PERSON: 'bg-purple-100 text-purple-700',
      ORGANIZATION: 'bg-blue-100 text-blue-700',
      LOCATION: 'bg-green-100 text-green-700',
      GPE: 'bg-cyan-100 text-cyan-700',
      DATE: 'bg-yellow-100 text-yellow-700',
      MONEY: 'bg-emerald-100 text-emerald-700',
      PRODUCT: 'bg-pink-100 text-pink-700',
    };
    return colors[type] || 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
        <Tag className="text-blue-500" size={24} />
        Named Entities
      </h3>

      <div className="space-y-4">
        {Object.entries(entities).map(([type, entityList]) => {
          if (!entityList || entityList.length === 0) return null;

          // Get unique entities
          const uniqueEntities = Array.from(new Set(entityList)).slice(0, 30);

          return (
            <div key={type} className="border-b border-gray-100 pb-4 last:border-b-0">
              <h4 className="text-sm font-semibold text-gray-700 mb-2">{type}</h4>
              <div className="flex flex-wrap gap-2">
                {uniqueEntities.map((entity, index) => (
                  <span
                    key={index}
                    className={`px-3 py-1 rounded-full text-xs font-medium ${getColorForType(type)}`}
                  >
                    {entity}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

