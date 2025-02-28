window.addEventListener("load", function() {
  const todosContainer = document.getElementById("todos-container");
  const todoForm = document.getElementById("todo-form");
  const todoInput = document.getElementById("todo-input");

  // Use relative URL; requests to /api/todos will be handled by Nginx proxy.
  const apiBaseUrl = "/api/todos";

  // Function to fetch and render todos from the backend.
  async function fetchTodos() {
    try {
      const response = await fetch(apiBaseUrl);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      renderTodos(data.todos);
    } catch (error) {
      console.error("Error fetching todos:", error);
      todosContainer.innerHTML = "<p>Error fetching todos.</p>";
    }
  }

  // Renders the list of todos into the DOM.
  function renderTodos(todos) {
    if (!Array.isArray(todos) || todos.length === 0) {
      todosContainer.innerHTML = "<p>No todos available.</p>";
      return;
    }
    todosContainer.innerHTML = "";
    const ul = document.createElement("ul");
    todos.forEach(todo => {
      const li = document.createElement("li");
      li.textContent = todo.task;
      ul.appendChild(li);
    });
    todosContainer.appendChild(ul);
  }

  // Adds a new todo by sending a POST request.
  async function addTodo(task) {
    try {
      const response = await fetch(apiBaseUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ task: task })
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      // After adding, reload the todos.
      await fetchTodos();
    } catch (error) {
      console.error("Error adding todo:", error);
    }
  }

  todoForm.addEventListener("submit", function(event) {
    event.preventDefault();
    const task = todoInput.value.trim();
    if (task) {
      addTodo(task);
      todoInput.value = "";
    }
  });

  // Initial load of todos.
  fetchTodos();
});
