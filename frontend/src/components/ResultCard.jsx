function ResultCard({ result }) {

    if (!result) {
        return null;
    }

    return (

        <div className="card mt-4 shadow-sm">

            <div className="card-body">

                <h4>Execution Result</h4>

                <hr />

                <p>

                    <strong>Selected Tool:</strong>

                    {result.tool}

                </p>

                <p>

                    <strong>Status:</strong>

                    {result.status}

                </p>

                <p>

                    <strong>Result:</strong>

                    {result.result.value}

                </p>

            </div>

        </div>

    );

}

export default ResultCard;