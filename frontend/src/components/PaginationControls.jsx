function PaginationControls({ currentPage, onPageChange, pageSize, totalItems }) {
  const totalPages = Math.max(1, Math.ceil(totalItems / pageSize));
  const isFirstPage = currentPage === 0;
  const isLastPage = currentPage >= totalPages - 1;

  return (
    <div className="pagination-controls">
      <span>
        Page {currentPage + 1} of {totalPages} ({totalItems} records)
      </span>

      <div className="pagination-buttons">
        <button
          disabled={isFirstPage}
          onClick={() => onPageChange(currentPage - 1)}
          type="button"
        >
          Previous
        </button>
        <button
          disabled={isLastPage}
          onClick={() => onPageChange(currentPage + 1)}
          type="button"
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default PaginationControls;
