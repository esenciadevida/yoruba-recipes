import { useEffect, useState } from 'react';
import { getCategories, createCategory, updateCategory, deleteCategory } from '../../api/categories';
import DataTable from '../../components/DataTable';
import Modal from '../../components/Modal';
import { FiEdit2, FiTrash2, FiPlus } from 'react-icons/fi';
import toast from 'react-hot-toast';
import CategoryForm from './CategoryForm';

export default function CategoryList() {
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [editingCategory, setEditingCategory] = useState(null);
    const [deleteId, setDeleteId] = useState(null);

    const fetchCategories = async () => {
        setLoading(true);
        try {
            const res = await getCategories();
            setCategories(res.data);
        } catch (err) {
            toast.error('Failed to load categories');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchCategories(); }, []);

    const handleSave = async (formData) => {
        try {
            if (editingCategory) {
                await updateCategory(editingCategory.id, formData);
                toast.success('Category updated');
            } else {
                await createCategory(formData);
                toast.success('Category created');
            }
            setShowForm(false);
            setEditingCategory(null);
            fetchCategories();
        } catch (err) {
            toast.error(err.response?.data?.detail || 'Error saving category');
        }
    };

    const handleDelete = async () => {
        try {
            await deleteCategory(deleteId);
            toast.success('Category deleted');
            setDeleteId(null);
            fetchCategories();
        } catch (err) {
            toast.error('Delete failed');
        }
    };

    const columns = [
        { header: 'Name', accessor: 'name' },
        { header: 'Description', accessor: 'description' },
        { header: 'Icon', accessor: 'icon' },
        {
            header: 'Actions',
            Cell: ({ row }) => (
                <div className="flex gap-3">
                    <button onClick={() => { setEditingCategory(row); setShowForm(true); }} className="text-blue-600 hover:text-blue-800">
                        <FiEdit2 className="text-lg" />
                    </button>
                    <button onClick={() => setDeleteId(row.id)} className="text-red-500 hover:text-red-700">
                        <FiTrash2 className="text-lg" />
                    </button>
                </div>
            ),
        },
    ];

    return (
        <div>
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                <h1 className="text-2xl font-bold text-dark-brown">Categories</h1>
                <button
                    onClick={() => { setEditingCategory(null); setShowForm(true); }}
                    className="flex items-center gap-2 bg-deep-green text-white px-5 py-3 rounded-xl hover:bg-deep-green/90 transition-all shadow-md shadow-deep-green/20"
                >
                    <FiPlus className="text-lg" /> Add Category
                </button>
            </div>

            <DataTable columns={columns} data={categories} loading={loading} />

            {showForm && (
                <Modal onClose={() => { setShowForm(false); setEditingCategory(null); }}>
                    <CategoryForm
                        initialData={editingCategory}
                        onSave={handleSave}
                        onCancel={() => { setShowForm(false); setEditingCategory(null); }}
                    />
                </Modal>
            )}

            {deleteId && (
                <Modal onClose={() => setDeleteId(null)}>
                    <div className="p-6 text-center">
                        <h3 className="text-xl font-semibold mb-2">Confirm Delete</h3>
                        <p className="text-gray-500 mb-6">This category will be permanently removed.</p>
                        <div className="flex justify-center gap-4">
                            <button onClick={() => setDeleteId(null)} className="px-6 py-2 bg-gray-200 rounded-lg hover:bg-gray-300">Cancel</button>
                            <button onClick={handleDelete} className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600">Delete</button>
                        </div>
                    </div>
                </Modal>
            )}
        </div>
    );
}