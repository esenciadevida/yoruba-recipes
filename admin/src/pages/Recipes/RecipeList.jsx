import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getRecipes, deleteRecipe } from '../../api/recipes';
import DataTable from '../../components/DataTable';
import Pagination from '../../components/Pagination';
import Modal from '../../components/Modal';
import { FiEdit2, FiTrash2, FiPlus, FiSearch } from 'react-icons/fi';
import toast from 'react-hot-toast';

export default function RecipeList() {
    const [recipes, setRecipes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [deleteId, setDeleteId] = useState(null);
    const limit = 10;

    const fetchRecipes = async () => {
        setLoading(true);
        try {
            const skip = (page - 1) * limit;
            const res = await getRecipes({ skip, limit, search: search || undefined });
            setRecipes(res.data);
            // use the total from the response, fallback to 0
            const total = res.total || 0;
            setTotalPages(Math.ceil(total / limit));
        } catch (err) {
            toast.error('Failed to load recipes');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRecipes();
    }, [page, search]);

    const handleDelete = async () => {
        try {
            await deleteRecipe(deleteId);
            toast.success('Recipe deleted');
            setDeleteId(null);
            fetchRecipes();
        } catch (err) {
            toast.error('Delete failed');
        }
    };

    const columns = [
        { header: 'Name', accessor: 'name' },
        { header: 'Category', accessor: 'category' },
        { header: 'Calories', accessor: 'calories' },
        { header: 'Difficulty', accessor: 'difficulty' },
        {
            header: 'Actions',
            Cell: ({ row }) => (
                <div className="flex gap-3">
                    <Link to={`/recipes/edit/${row.id}`} className="text-blue-600 hover:text-blue-800">
                        <FiEdit2 className="text-lg" />
                    </Link>
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
                <h1 className="text-2xl font-bold text-dark-brown">Recipes</h1>
                <Link
                    to="/recipes/new"
                    className="flex items-center gap-2 bg-terracotta text-white px-5 py-3 rounded-xl hover:bg-terracotta/90 transition-all shadow-md shadow-terracotta/20"
                >
                    <FiPlus className="text-lg" /> Add Recipe
                </Link>
            </div>

            <div className="relative mb-6">
                <FiSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
                <input
                    type="text"
                    placeholder="Search recipes..."
                    value={search}
                    onChange={(e) => { setSearch(e.target.value); setPage(1); }}
                    className="w-full sm:w-80 pl-10 pr-4 py-3 bg-white rounded-xl border border-gray-200 focus:ring-2 focus:ring-terracotta focus:border-transparent outline-none transition-all"
                />
            </div>

            <DataTable columns={columns} data={recipes} loading={loading} />

            <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />

            {deleteId && (
                <Modal onClose={() => setDeleteId(null)}>
                    <div className="p-6 text-center">
                        <h3 className="text-xl font-semibold mb-2">Confirm Delete</h3>
                        <p className="text-gray-500 mb-6">This action cannot be undone.</p>
                        <div className="flex justify-center gap-4">
                            <button onClick={() => setDeleteId(null)} className="px-6 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors">
                                Cancel
                            </button>
                            <button onClick={handleDelete} className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors">
                                Delete
                            </button>
                        </div>
                    </div>
                </Modal>
            )}
        </div>
    );
}