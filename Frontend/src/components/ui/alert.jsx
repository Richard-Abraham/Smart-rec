import * as React from "react";
import { cn } from "../../lib/utils";

const Alert = ({ variant = "info", className, children, ...props }) => {
  const variantClasses = {
    info: "bg-blue-100 text-blue-800",
    success: "bg-green-100 text-green-800",
    warning: "bg-yellow-100 text-yellow-800",
    destructive: "bg-red-100 text-red-800",
  };

  return (
    <div
      className={cn(
        "p-4 rounded-md",
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

const AlertDescription = ({ className, children, ...props }) => (
  <p className={cn("text-sm", className)} {...props}>
    {children}
  </p>
);

export { Alert, AlertDescription };