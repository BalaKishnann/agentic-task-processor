import { Component } from "react";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render shows the fallback UI.
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Rendering errors don't go through the API-call try/catch paths
    // elsewhere in the app — this is the only place that catches a
    // component actually throwing during render. Logged to console
    // for now; wire to a real error-reporting service (Sentry, etc.)
    // here if/when one is added.
    console.error("Uncaught error in component tree:", error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback(this.state.error, this.handleReset);
      }

      return (
        <div className="alert alert-danger m-3" role="alert">
          <h5 className="alert-heading">Something went wrong</h5>
          <p className="mb-2">
            {this.props.message ||
              "This part of the app hit an unexpected error."}
          </p>
          <button
            className="btn btn-sm btn-outline-danger"
            onClick={this.handleReset}
          >
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
