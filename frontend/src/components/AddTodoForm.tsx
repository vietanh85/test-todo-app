import React, { useState } from 'react';
import { useCreateTodo } from '../hooks/useTodos';
import { Button } from './ui/Button';
import { Input } from './ui/Input';
import { Plus } from 'lucide-react';

export const AddTodoForm: React.FC = () => {
  const [title, setTitle] = useState('');
  const createTodo = useCreateTodo();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    createTodo.mutate({ title: title.trim() }, {
      onSuccess: () => {
        setTitle('');
      }
    });
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <Input
        placeholder="Add a new task..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="flex-1"
        disabled={createTodo.isPending}
      />
      <Button type="submit" disabled={createTodo.isPending || !title.trim()}>
        <Plus className="w-4 h-4 mr-2" />
        Add
      </Button>
    </form>
  );
};
