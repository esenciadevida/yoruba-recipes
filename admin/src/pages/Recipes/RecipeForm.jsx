import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getRecipe, createRecipe, updateRecipe } from '../../api/recipes';
import { getCategories } from '../../api/categories';
import toast from 'react-hot-toast';
import { FiPlus, FiTrash2 } from 'react-icons/fi';

export default function RecipeForm() {
    const { id } = useParams();
    const isEdit = Boolean(id);
    const navigate = useNavigate();
    const [categories, setCategories] = useState([]);
    const [form, setForm] = useState({
        name: '', local_name: '', category: '', calories: 0, protein: 0,
        carbohydrates: 0, fat: 0, fiber: 0, glycemic_index: '', calorie_density: '',
        recommended_portion: '', difficulty: 'easy', origin: '', tags: [], ingredients: [],
        health_benefits: [],
    });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        getCategories().then(res => setCategories(res.data));
        if (isEdit) {
            getRecipe(id).then(res => setForm(res.data)).catch(() => toast.error('Failed to load recipe'));
        }
    }, [id]);

    const handleChange = (e) => {
        const { name, value, type } = e.target;
        const newValue = type === 'number' ? Number(value) : value;
        setForm(prev => ({ ...prev, [name]: newValue }));
    };

    const handleArrayChange = (field, index, newValue) => {
        const arr = [...form[field]];
        arr[index] = newValue;
        setForm(prev => ({ ...prev, [field]: arr }));
    };

    const addArrayItem = (field, template) => {
        setForm(prev => ({ ...prev, [field]: [...prev[field], template] }));
    };

    const removeArrayItem = (field, index) => {
        const arr = [...form[field]];
        arr.splice(index, 1);
        setForm(prev => ({ ...prev, [field]: arr }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            if (isEdit) {
                await updateRecipe(id, form);
                toast.success('Recipe updated');
            } else {
                await createRecipe(form);
                toast.success('Recipe created');
            }
            navigate('/recipes');
        } catch (err) {
            toast.error(err.response?.data?.detail || 'Error saving recipe');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-5xl mx-auto">
            <h1 className="text-2xl font-bold text-dark-brown mb-6">{isEdit ? 'Edit Recipe' : 'New Recipe'}</h1>
            <form onSubmit={handleSubmit} className="space-y-8">
                {/* Basic Info Section */}
                <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
                    <h2 className="text-lg font-semibold mb-4 text-dark-brown">Basic Information</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Input label="Name *" name="name" value={form.name} onChange={handleChange} required />
                        <Input label="Local Name" name="local_name" value={form.local_name} onChange={handleChange} />
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Category *</label>
                            <select name="category" value={form.category} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-terracotta focus:border-transparent">
                                <option value="">Select category</option>
                                {categories.map(cat => <option key={cat.id} value={cat.name}>{cat.name}</option>)}
                            </select>
                        </div>
                        <Input label="Origin" name="origin" value={form.origin} onChange={handleChange} />
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Difficulty</label>
                            <select name="difficulty" value={form.difficulty} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-2.5">
                                <option>easy</option><option>medium</option><option>hard</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Nutrition Section */}
                <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
                    <h2 className="text-lg font-semibold mb-4 text-dark-brown">Nutritional Information</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <Input label="Calories" name="calories" type="number" value={form.calories} onChange={handleChange} />
                        <Input label="Protein (g)" name="protein" type="number" value={form.protein} onChange={handleChange} />
                        <Input label="Carbs (g)" name="carbohydrates" type="number" value={form.carbohydrates} onChange={handleChange} />
                        <Input label="Fat (g)" name="fat" type="number" value={form.fat} onChange={handleChange} />
                        <Input label="Fiber (g)" name="fiber" type="number" value={form.fiber} onChange={handleChange} />
                        <Input label="Glycemic Index" name="glycemic_index" value={form.glycemic_index} onChange={handleChange} />
                        <Input label="Calorie Density" name="calorie_density" value={form.calorie_density} onChange={handleChange} />
                        <Input label="Recommended Portion" name="recommended_portion" value={form.recommended_portion} onChange={handleChange} />
                    </div>
                </div>

                {/* Ingredients Section */}
                <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
                    <h2 className="text-lg font-semibold mb-4 text-dark-brown">Ingredients</h2>
                    {form.ingredients.map((ing, i) => (
                        <div key={i} className="flex gap-2 mb-2">
                            <input placeholder="Name" value={ing.name} onChange={e => handleArrayChange('ingredients', i, { ...ing, name: e.target.value })} className="flex-1 border border-gray-300 rounded-lg p-2.5" />
                            <input placeholder="Qty" value={ing.quantity} onChange={e => handleArrayChange('ingredients', i, { ...ing, quantity: e.target.value })} className="w-24 border border-gray-300 rounded-lg p-2.5" />
                            <button type="button" onClick={() => removeArrayItem('ingredients', i)} className="text-red-500 hover:text-red-700 p-2"><FiTrash2 /></button>
                        </div>
                    ))}
                    <button type="button" onClick={() => addArrayItem('ingredients', { name: '', quantity: '' })} className="flex items-center gap-1 text-terracotta hover:text-terracotta/80 text-sm font-medium mt-2">
                        <FiPlus /> Add ingredient
                    </button>
                </div>

                {/* Health Benefits Section */}
                <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
                    <h2 className="text-lg font-semibold mb-4 text-dark-brown">Health Benefits</h2>
                    {form.health_benefits.map((b, i) => (
                        <div key={i} className="flex gap-2 mb-2">
                            <input value={b} onChange={e => handleArrayChange('health_benefits', i, e.target.value)} className="flex-1 border border-gray-300 rounded-lg p-2.5" />
                            <button type="button" onClick={() => removeArrayItem('health_benefits', i)} className="text-red-500 p-2"><FiTrash2 /></button>
                        </div>
                    ))}
                    <button type="button" onClick={() => addArrayItem('health_benefits', '')} className="flex items-center gap-1 text-terracotta text-sm font-medium mt-2">
                        <FiPlus /> Add benefit
                    </button>
                </div>

                <button type="submit" disabled={loading} className="w-full py-4 bg-terracotta text-white font-semibold rounded-xl hover:bg-terracotta/90 transition-colors shadow-lg shadow-terracotta/20 disabled:opacity-50">
                    {loading ? 'Saving...' : isEdit ? 'Update Recipe' : 'Create Recipe'}
                </button>
            </form>
        </div>
    );
}

const Input = ({ label, ...props }) => (
    <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
        <input className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-terracotta focus:border-transparent" {...props} />
    </div>
);