document.addEventListener('DOMContentLoaded', () => {
    fetchCourses();
});

const form = document.getElementById('course-form');
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const courseId = document.getElementById('course-id').value;
    const courseName = document.getElementById('course-name').value;
    const method = courseId ? 'PUT' : 'POST';
    const url = courseId ? `http://127.0.0.1:5000/courses/${courseId}` : 'http://127.0.0.1:5000/courses';

    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
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
    const response = await fetch('http://127.0.0.1:5000/courses');
    const courses = await response.json();
    const tableBody = document.getElementById('courses-table').querySelector('tbody');
    tableBody.innerHTML = '';
    courses.forEach(course => {
        const row = tableBody.insertRow();
        row.innerHTML = `
            <td>${course.id}</td>
            <td>${course.name}</td>
            <td>
                <button onclick="editCourse(${course.id}, '${course.name}')">Editar</button>
                <button onclick="deleteCourse(${course.id})">Excluir</button>
            </td>
        `;
    });
}

function editCourse(id, name) {
    document.getElementById('course-id').value = id;
    document.getElementById('course-name').value = name;
}

async function deleteCourse(id) {
    if (confirm('Tem certeza que deseja excluir este curso?')) {
        const response = await fetch(`http://127.0.0.1:5000/courses/${id}`, { method: 'DELETE' });
        const data = await response.json();
        alert(data.message);
        if (data.success) {
            fetchCourses();
        }
    }
}