import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useTodos } from './hooks/useTodos';
import { TodoItem } from './components/TodoItem';
import { AddTodoForm } from './components/AddTodoForm';
import { LoginPage } from './components/LoginPage';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { Button } from './components/ui/Button';
import { Loader2, ListTodo, LogOut } from 'lucide-react';

const queryClient = new QueryClient();

function TodoApp() {
  const { data: todos, isLoading, isError, error } = useTodos();
  const { logout } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <ListTodo className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Todo App</h1>
          </div>
          <Button variant="ghost" size="icon" onClick={logout} title="Logout">
            <LogOut className="w-5 h-5 text-slate-500" />
          </Button>
        </div>

        <div className="space-y-6">
          <AddTodoForm />

          <div className="space-y-3">
            {isLoading ? (
              <div className="flex justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
              </div>
            ) : isError ? (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md text-sm">
                Error loading todos: {(error as Error).message}
              </div>
            ) : todos && todos.length > 0 ? (
              todos.map((todo) => (
                <TodoItem key={todo.id} todo={todo} />
              ))
            ) : (
              <div className="text-center py-12 text-slate-500 bg-white border border-dashed border-slate-300 rounded-lg">
                No todos yet. Add one to get started!
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function Main() {
  const { token, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-12 h-12 animate-spin text-blue-500" />
      </div>
    );
  }

  if (!token) {
    return <LoginPage />;
  }

  return <TodoApp />;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Main />
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
