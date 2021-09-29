$(document).ready(() => {
    $('.delete-button').click((event) => {
        event.preventDefault();
        $.ajax({
            url: '/delete',
            type: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({fileName: event.target.id}),
            success: () => {
                window.location.reload()
            }
        })
    })
})