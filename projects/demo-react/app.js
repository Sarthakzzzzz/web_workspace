const { useState } = React;

function App() {
    const [count, setCount] = useState(0);
    const [todos, setTodos] = useState([]);
    const [inputValue, setInputValue] = useState('');

    const addTodo = () => {
        if (inputValue.trim()) {
            setTodos([...todos, { id: Date.now(), text: inputValue, completed: false }]);
            setInputValue('');
        }
    };

    const toggleTodo = (id) => {
        setTodos(todos.map(todo => 
            todo.id === id ? { ...todo, completed: !todo.completed } : todo
        ));
    };

    const deleteTodo = (id) => {
        setTodos(todos.filter(todo => todo.id !== id));
    };

    return (
        <div className="app">
            <header className="app-header">
                <h1>🚀 Web_Workspace Demo</h1>
                <p>Full-Stack Development Environment</p>
            </header>

            <div className="demo-section">
                <h2>Counter Demo</h2>
                <div className="counter">
                    <button onClick={() => setCount(count - 1)}>-</button>
                    <span className="count">{count}</span>
                    <button onClick={() => setCount(count + 1)}>+</button>
                </div>
            </div>

            <div className="demo-section">
                <h2>Todo List Demo</h2>
                <div className="todo-input">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && addTodo()}
                        placeholder="Add a new todo..."
                    />
                    <button onClick={addTodo}>Add</button>
                </div>
                <ul className="todo-list">
                    {todos.map(todo => (
                        <li key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                            <span onClick={() => toggleTodo(todo.id)}>{todo.text}</span>
                            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
                        </li>
                    ))}
                </ul>
            </div>

            <div className="demo-section">
                <h3>✨ Features Demonstrated:</h3>
                <ul className="features">
                    <li>✅ React Hooks (useState)</li>
                    <li>✅ Event Handling</li>
                    <li>✅ Conditional Rendering</li>
                    <li>✅ List Rendering</li>
                    <li>✅ CSS Styling</li>
                    <li>✅ Interactive Components</li>
                </ul>
            </div>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));