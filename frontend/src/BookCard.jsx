// BookCard.jsx
// This component is used to display a book card. It takes in the index of the book, the book object, and functions for deleting, editing, and incrementing the current page of the book. It also takes in a cover image for the book.
function BookCard({ index, book, onDelete, onEdit, onIncrement, cover }) {
    return (
        <div className="book-item">
            <img className="image" src={cover} alt={book.title} />
            <div className="book-info">
                <h4 className="h4InLine">Book {index + 1}</h4>
                <h2 className="h2InLine">{book.title}</h2>
                <div className="page-row">
                    <h3 className="h3InLine">Page {book.current_page} of {book.total_pages}</h3>
                    <button className="increment-btn" onClick={() => onIncrement(book)}>+</button>
                </div>
                <button className="delete-btn" onClick={() => onDelete(book.title)}>Delete</button>
                <button className="edit-btn" onClick={() => onEdit(book)}>Edit</button>
            </div>
        </div>
    )
}

export default BookCard
