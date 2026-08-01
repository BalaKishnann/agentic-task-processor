function TracePanel({ trace }) {

    if (!trace) {
        return null;
    }

    return (

        <div className="card mt-4 shadow-sm">

            <div className="card-body">

                <h4>Execution Trace</h4>

                <hr />

                <ul className="list-group">

                    {trace.map((step, index) => (

                        <li
                            key={index}
                            className="list-group-item"
                        >

                            ✅ {step}

                        </li>

                    ))}

                </ul>

            </div>

        </div>

    );

}

export default TracePanel;