$('.delete-cupcake').click(deleteCupcake)

async function deleteCupcake() {
   const id = $(this).data('id')
   await axios.delete(`/api/cupcakeCipcakes/${id}`)
   // alert("DELETED!!!")
   $(this).parent().remove()
}
