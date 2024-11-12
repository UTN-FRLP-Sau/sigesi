function cambiarCurso(select, estudianteId) {
  const cursoId = select.value;

  fetch(`/inscripcion/cambiar_curso/${estudianteId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `curso_id=${cursoId}`,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "ok") {
        alert("Curso cambiado correctamente.");
      } else {
        alert("Error al cambiar el curso.");
      }
    });
}
