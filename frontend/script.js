window.addEventListener("load", function() {
  const todosContainer = document.getElementById("todos-container");
  const todoForm = document.getElementById("todo-form");
  const todoInput = document.getElementById("todo-input");

  // API endpoint
  const apiBaseUrl = "/api/todos";

  // Function to fetch and render todos
  async function fetchTodos() {
    try {
      todosContainer.innerHTML = "<p>Loading todos...</p>";
      const response = await fetch(apiBaseUrl);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      renderTodos(data.todos);
    } catch (error) {
      console.error("Error fetching todos:", error);
      todosContainer.innerHTML = "<p class='error'>Error fetching todos. Please try again.</p>";
    }
  }

  // Renders the list of todos
  function renderTodos(todos) {
    if (!Array.isArray(todos) || todos.length === 0) {
      todosContainer.innerHTML = "<p>No todos available. Add your first one!</p>";
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

  // Adds a new todo
  async function addTodo(task) {
    try {
      const button = todoForm.querySelector('button');
      button.disabled = true;
      button.textContent = 'Adding...';
      
      const response = await fetch(apiBaseUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ task: task })
      });
      
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      
      // After adding, reload the todos
      await fetchTodos();
    } catch (error) {
      console.error("Error adding todo:", error);
    } finally {
      button.disabled = false;
      button.textContent = 'Add Todo';
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

  // Initial load of todos
  fetchTodos();
});