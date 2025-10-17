import { useLocation, useNavigate } from "react-router-dom";

const ApplicationResult = () => {
    // Gather router data
    const { state } = useLocation();
    const navigate = useNavigate();

    // If no state or application data, show message and back button
    if (!state || !state.application) {
        return (
            <div className="p-6 text-center">
                <p>No application data found.</p>
                <button
                    onClick={() => navigate("/")}
                    className="mt-4 bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
                >
                    Go Back
                </button>
            </div>
        );
    }

    // Check for approval status
    const app = state.application;
    const isApproved = app.status.toLowerCase() === "approved";

    return (
        <div className="p-6 max-w-lg mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Application Result</h2>

            {/* Render Results */}
            <div className="bg-gray-100 p-4 rounded shadow">
                <p>
                    <strong>Status:</strong>{" "}
                    <span
                        className={
                            isApproved ? "text-green-600" : "text-red-600"
                        }
                    >
                        {app.status}
                    </span>
                </p>

                {/* Render conditional portions based on approved or denied status */}
                {isApproved ? (
                    <>
                        <p>
                            <strong>Approved Amount:</strong> $
                            {app.approved_amount?.toFixed(2)} 
                        </p>
                        <p>
                            <strong>Interest Rate:</strong> {app.interest_rate}%
                        </p>
                        <p>
                            <strong>Monthly Payment:</strong> $
                            {app.monthly_payment?.toFixed(2)}
                        </p>
                        <p>
                            <strong>Term (Months):</strong> {app.term_months}
                        </p>
                    </>
                ) : (
                    <p>
                        <strong>Reason:</strong>{" "}
                        {app.reason ||
                            "You can not be approved at this time. Please call 555-555-5555 for more information."}
                    </p>
                )}
            </div>

            <button
                onClick={() => navigate("/")}
                className="mt-6 bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
            >
                Apply Again
            </button>
        </div>
    );
};

export default ApplicationResult;
