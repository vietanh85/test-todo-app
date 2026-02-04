import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as todoApi from '../api/todos';
import type { Todo } from '../types/todo';

export const useTodos = () => {
  return useQuery({
    queryKey: ['todos'],
    queryFn: todoApi.fetchTodos,
  });
};

export const useCreateTodo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: todoApi.createTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
};

export const useUpdateTodo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: todoApi.updateTodo,
    onMutate: async (updatedTodo) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      const previousTodos = queryClient.getQueryData<Todo[]>(['todos']);

      queryClient.setQueryData<Todo[]>(['todos'], (old) =>
        old?.map((todo) =>
          todo.id === updatedTodo.id ? { ...todo, ...updatedTodo } : todo
        )
      );

      return { previousTodos };
    },
    onError: (_err, _newTodo, context) => {
      queryClient.setQueryData(['todos'], context?.previousTodos);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
};

export const useDeleteTodo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: todoApi.deleteTodo,
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      const previousTodos = queryClient.getQueryData<Todo[]>(['todos']);

      queryClient.setQueryData<Todo[]>(['todos'], (old) =>
        old?.filter((todo) => todo.id !== id)
      );

      return { previousTodos };
    },
    onError: (_err, _id, context) => {
      queryClient.setQueryData(['todos'], context?.previousTodos);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });
};
