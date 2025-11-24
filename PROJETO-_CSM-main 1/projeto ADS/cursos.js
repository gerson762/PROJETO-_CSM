document.addEventListener('DOMContentLoaded', fetchCourses);

const form = document.getElementById('course-form');
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const courseId = document.getElementById('course-id').value;
    const courseName = document.getElementById('course-name').value;
    const method = courseId ? 'PUT' : 'POST';
    const url = courseId ? `/courses/${courseId}` : '/courses'; // <-- CORRIGIDO

    const response = await fetch(url, {
        method: method,
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem('userRole')
        },
        body: JSON.stringify({ name: courseName })
    });
    const data = await response.json();
    alert(data.message);
    if (data.success) {
        form.reset();
        document.getElementById('course-id').value = '';
        fetchCourses();
    }
});

async function fetchCourses() {
    const response = await fetch('/courses'); // <-- CORRIGIDO
    const courses = await response.json();
    const tableBody = document.getElementById('courses-table').querySelector('tbody');
    tableBody.innerHTML = '';
    const userRole = localStorage.getItem('userRole');

    courses.forEach(course => {
        const row = tableBody.insertRow();
        let actions = '';
        if (userRole === 'admin') {
            actions = `<button onclick="editCourse(${course.id}, '${course.name}')">Editar</button> 
                       <button onclick="deleteCourse(${course.id})">Excluir</button>`;
        }
        row.innerHTML = `<td>${course.id}</td><td>${course.name}</td><td>${actions}</td>`;
    });
}
// Funções editCourse e deleteCourse devem seguir a mesma lógica...
window.editCourse = function(id, name) {
    document.getElementById('course-id').value = id;
    document.getElementById('course-name').value = name;
}
window.deleteCourse = async function(id) {
    if (confirm('Excluir?')) {
        const response = await fetch(`/courses/${id}`, { method: 'DELETE' }); // <-- CORRIGIDO
        const data = await response.json();
        alert(data.message);
        fetchCourses();
    }
}