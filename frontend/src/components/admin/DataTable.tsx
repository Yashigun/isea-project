"use client";

import { Pencil, Trash2 } from "lucide-react";

// inside DataTable.tsx
interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  onEdit?: (row: T) => void;
  onDelete?: (row: T) => void;
  deleteLabel?: string;
}
// Then in the actions cell:
{onDelete && (
  <button onClick={() => onDelete(row)} className="text-red-600 hover:text-red-800">
    <Trash2 size={18} />
    {deleteLabel && <span className="ml-1 text-sm">{deleteLabel}</span>}
  </button>
)}

export default function DataTable<T extends { public_id: string }>({
  columns,
  data,
  onEdit,
  onDelete,
}: DataTableProps<T>) {
  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow">
      <table className="w-full">
        <thead className="bg-gray-50 border-b">
          <tr>
            {columns.map((col) => (
              <th key={String(col.key)} className="text-left px-6 py-3 text-sm font-medium text-gray-500">
                {col.label}
              </th>
            ))}
            {(onEdit || onDelete) && <th className="px-6 py-3 text-right">Actions</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.public_id} className="border-b hover:bg-gray-50">
              {columns.map((col) => (
                <td key={String(col.key)} className="px-6 py-4">
                  {col.render ? col.render(row[col.key], row) : String(row[col.key])}
                </td>
              ))}
              {(onEdit || onDelete) && (
                <td className="px-6 py-4 text-right space-x-2">
                  {onEdit && (
                    <button onClick={() => onEdit(row)} className="text-blue-600 hover:text-blue-800">
                      <Pencil size={18} />
                    </button>
                  )}
                  {onDelete && (
                    <button onClick={() => onDelete(row)} className="text-red-600 hover:text-red-800">
                      <Trash2 size={18} />
                    </button>
                  )}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}