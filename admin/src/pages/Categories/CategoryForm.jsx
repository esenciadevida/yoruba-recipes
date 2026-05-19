import { useState } from 'react';

export default function CategoryForm({ initialData, onSave, onCancel }) {
    const [form, setForm] = useState({
        name: initialData?.name || '',
        description: initialData?.description || '',
        icon: initialData?.icon || '',
    });
    const [saving, setSaving] = useState(false);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        await onSave(form);
        setSaving(false);
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="p-6 bg-white dark:bg-gray-800 rounded-xl w-full max-w-md mx-auto"
        >
            <h2 className="text-xl font-bold mb-4">
                {initialData ? 'Edit Category' : 'New Category'}
            </h2>
            <div className="space-y-4">
                <div>
                    <label className="block text-sm font-medium">Name *</label>
                    <input
                        name="name"
                        value={form.name}
                        onChange={handleChange}
                        required
                        className="w-full border rounded-lg p-2 dark:bg-gray-700"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium">Description</label>
                    <input
                        name="description"
                        value={form.description}
                        onChange={handleChange}
                        className="w-full border rounded-lg p-2 dark:bg-gray-700"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium">
                        Icon (React Icons name, e.g., FiGrid)
                    </label>
                    <input
                        name="icon"
                        value={form.icon}
                        onChange={handleChange}
                        className="w-full border rounded-lg p-2 dark:bg-gray-700"
                    />
                </div>
            </div>
            <div className="flex justify-end gap-3 mt-6">
                <button
                    type="button"
                    onClick={onCancel}
                    className="px-4 py-2 bg-gray-200 rounded-lg"
                >
                    Cancel
                </button>
                <button
                    type="submit"
                    disabled={saving}
                    className="px-4 py-2 bg-terracotta text-white rounded-lg disabled:opacity-50"
                >
                    {saving ? 'Saving...' : 'Save'}
                </button>
            </div>
        </form>
    );
}