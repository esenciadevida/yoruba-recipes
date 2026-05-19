import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import AdminLayout from './components/Layout/AdminLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import RecipeList from './pages/Recipes/RecipeList';
import RecipeForm from './pages/Recipes/RecipeForm';
import CategoryList from './pages/Categories/CategoryList';
import NotFound from './pages/NotFound';

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AdminLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="recipes" element={<RecipeList />} />
            <Route path="recipes/new" element={<RecipeForm />} />
            <Route path="recipes/edit/:id" element={<RecipeForm />} />
            <Route path="categories" element={<CategoryList />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}