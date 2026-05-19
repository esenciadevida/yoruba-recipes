import { FiLoader } from 'react-icons/fi';

export default function DataTable({ columns, data, loading }) {
    if (loading) {
        return (
            <div className="flex justify-center py-12">
                <FiLoader className="animate-spin text-3xl text-terracotta" />
            </div>
        );
    }

    if (!data || data.length === 0) {
        return (
            <div className="text-center py-12 bg-white rounded-2xl shadow-sm border border-gray-100">
                <p className="text-gray-500">No data found.</p>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-100">
                    <thead>
                        <tr className="bg-gray-50">
                            {columns.map((col) => (
                                <th
                                    key={col.header}
                                    className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider"
                                >
                                    {col.header}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-50">
                        {data.map((row, i) => (
                            <tr
                                key={row.id || i}
                                className="hover:bg-gray-50 transition-colors duration-150"
                            >
                                {columns.map((col) => (
                                    <td
                                        key={col.header}
                                        className="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
                                    >
                                        {col.Cell ? <col.Cell row={row} /> : row[col.accessor]}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}