"use client";

import { Pencil, Trash2 } from "lucide-react";

export interface Column<T> {
  key: keyof T;
  label: string;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
}

interface DataTableProps<T extends { public_id: string }> {
  columns: Column<T>[];
  data: T[];
  onEdit?: (row: T) => void;
  onDelete?: (row: T) => void;
  deleteLabel?: string;
}

export default function DataTable<T extends { public_id: string }>({
  columns,
  data,
  onEdit,
  onDelete,
  deleteLabel,
}: DataTableProps<T>) {
  return (
    <div className="overflow-x-auto rounded-lg bg-white shadow">
      <table className="w-full">
        <thead className="border-b bg-gray-50">
          <tr>
            {columns.map((col) => (
              <th
                key={String(col.key)}
                className="px-3 py-2 text-left text-xs font-medium text-gray-500 sm:px-6 sm:py-3 sm:text-sm"
              >
                {col.label}
              </th>
            ))}

            {(onEdit || onDelete) && (
              <th className="px-3 py-2 text-right text-xs sm:px-6 sm:py-3 sm:text-sm">
                Actions
              </th>
            )}
          </tr>
        </thead>

        <tbody>
          {data.map((row) => (
            <tr
              key={row.public_id}
              className="border-b hover:bg-gray-50"
            >
              {columns.map((col) => (
                <td
                  key={String(col.key)}
                  className="px-3 py-3 text-sm sm:px-6 sm:py-4 sm:text-base"
                >
                  {col.render
                    ? col.render(row[col.key], row)
                    : String(row[col.key] ?? "")}
                </td>
              ))}

              {(onEdit || onDelete) && (
                <td className="space-x-2 px-3 py-3 text-right sm:px-6 sm:py-4">
                  {onEdit && (
                    <button
                      onClick={() => onEdit(row)}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <Pencil size={18} />
                    </button>
                  )}

                  {onDelete && (
                    <button
                      onClick={() => onDelete(row)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <Trash2 size={18} />

                      {deleteLabel && (
                        <span className="ml-1 text-sm">
                          {deleteLabel}
                        </span>
                      )}
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
