const API = "http://127.0.0.1:8000";

// CREATE USER
async function createUser() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;

  await fetch(`${API}/users`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      name: name,
      email: email,
    }),
  });

  getUsers();
}

// GET ALL USERS
async function getUsers() {
  const res = await fetch(`${API}/users/`);
  const users = await res.json();

  const container = document.getElementById("users");

  container.innerHTML = "";

  users.forEach((user) => {
    container.innerHTML += `
<div class="user">

<span>
${user.id} - ${user.name} (${user.email})
</span>

<div>
<button onclick="updateUser(${user.id})">Edit</button>
<button onclick="deleteUser(${user.id})">Delete</button>
</div>

</div>
`;
  });
}

// DELETE USER
async function deleteUser(id) {
  await fetch(`${API}/users/${id}`, {
    method: "DELETE",
  });

  getUsers();
}

// UPDATE USER
async function updateUser(id) {
  const name = prompt("Enter new name");
  const email = prompt("Enter new email");

  await fetch(`${API}/users/${id}`, {
    method: "PUT",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      name: name,
      email: email,
    }),
  });

  getUsers();
}
