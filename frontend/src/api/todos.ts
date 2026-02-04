import api from '../lib/api';
import type { Todo, TodoCreate, TodoUpdate } from '../types/todo';

export const fetchTodos = async (): Promise<Todo[]> => {
  const { data } = await api.get<Todo[]>('/todos');
  return data;
};

export const createTodo = async (todo: TodoCreate): Promise<Todo> => {
  const { data } = await api.post<Todo>('/todos', todo);
  return data;
};

export const updateTodo = async ({ id, ...todo }: { id: number } & TodoUpdate): Promise<Todo> => {
  const { data } = await api.put<Todo>(`/todos/${id}`, todo);
  return data;
};

export const deleteTodo = async (id: number): Promise<void> => {
  await api.delete(`/todos/${id}`);
};
