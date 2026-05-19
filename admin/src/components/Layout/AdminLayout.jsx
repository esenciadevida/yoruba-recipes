import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import { Toaster } from 'react-hot-toast';

export default function AdminLayout() {
    return (
        <div className="flex min-h-screen bg-gray-50">
            <Sidebar />
            <main className="flex-1 p-6 lg:p-8 pt-20 lg:pt-8 overflow-x-hidden">
                <Outlet />
            </main>
            <Toaster position="top-right" toastOptions={{
                style: { background: '#1A1A1A', color: '#fff', borderRadius: '12px' },
            }} />
        </div>
    );
}