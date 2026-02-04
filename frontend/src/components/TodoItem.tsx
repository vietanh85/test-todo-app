import React from 'react';
import type { Todo } from '../types/todo';
import { useUpdateTodo, useDeleteTodo } from '../hooks/useTodos';
import { Button } from './ui/Button';
import { Check, Trash2, Square } from 'lucide-react';
import { cn } from '../lib/utils';

interface TodoItemProps {
  todo: Todo;
}

export const TodoItem: React.FC<TodoItemProps> = ({ todo }) => {
  const updateTodo = useUpdateTodo();
  const deleteTodo = useDeleteTodo();

  const toggleComplete = () => {
    updateTodo.mutate({ id: todo.id, completed: !todo.completed });
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      deleteTodo.mutate(todo.id);
    }
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white border border-slate-200 rounded-lg shadow-sm group">
      <div className="flex items-center space-x-3 overflow-hidden">
        <button
          onClick={toggleComplete}
          aria-label={todo.completed ? "Mark as incomplete" : "Mark as complete"}
          className={cn(
            "flex-shrink-0 transition-colors",
            todo.completed ? "text-green-500" : "text-slate-400 hover:text-blue-500"
          )}
        >
          {todo.completed ? <Check className="w-6 h-6" /> : <Square className="w-6 h-6" />}
        </button>
        <div className="overflow-hidden">
          <h3 className={cn(
            "text-sm font-medium transition-all",
            todo.completed ? "line-through text-slate-400" : "text-slate-900"
          )}>
            {todo.title}
          </h3>
          {todo.description && (
            <p className={cn(
              "text-xs truncate",
              todo.completed ? "text-slate-300" : "text-slate-500"
            )}>
              {todo.description}
            </p>
          )}
        </div>
      </div>
      <Button
        variant="ghost"
        size="icon"
        onClick={handleDelete}
        aria-label="Delete todo"
        className="opacity-0 group-hover:opacity-100 text-slate-400 hover:text-red-500 transition-opacity"
      >
        <Trash2 className="w-4 h-4" />
      </Button>
    </div>
  );
};
