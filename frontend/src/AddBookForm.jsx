// AddBookForm.jsx
// This component is used to add a new book. It takes in the new title, current page, and total pages of the book, as well as their respective setter functions. It also takes in an onSubmit function that is called when the user clicks the "Add Book" button, and an editingBook prop that determines whether the form is being used to edit an existing book or add a new one.
function AddBookForm({ newTitle, setNewTitle, newCurrentPage, setNewCurrentPage, newTotalPages, setNewTotalPages, onSubmit, editingBook }) {
    return (
        <div className="add-book">
            <input
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                placeholder="Book title"
            />
            <input
                value={newCurrentPage}
                onChange={(e) => setNewCurrentPage(e.target.value)}
                placeholder="Current page"
                type="number"
            />
            <input
                value={newTotalPages}
                onChange={(e) => setNewTotalPages(e.target.value)}
                placeholder="Total pages"
                type="number"
            />
            <button onClick={onSubmit}>{editingBook ? "Update Book" : "Add Book"}</button>
        </div>
    )
}

export default AddBookForm
