function HistoryTable({ history }) {
  if (!history || history.length === 0) {
    return null;
  }

  return (
    <div className="card mt-4 shadow-sm">
      <div className="card-body">
        <h4>Task History</h4>

        <table className="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Task</th>
              <th>Tool</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {history.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>

                <td>{item.task}</td>

                <td>{item.tool}</td>

                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default HistoryTable;
