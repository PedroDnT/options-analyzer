import React from 'react'

export const Alert = ({ children, className = '', variant = 'default', ...props }) => {
  const baseClasses = 'relative w-full rounded-lg border p-4'
  
  const variants = {
    default: 'bg-background text-foreground',
    destructive: 'border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive'
  }
  
  return (
    <div className={`${baseClasses} ${variants[variant]} ${className}`} {...props}>
      {children}
    </div>
  )
}

export const AlertTitle = ({ children, className = '', ...props }) => {
  return (
    <h5 className={`mb-1 font-medium leading-none tracking-tight ${className}`} {...props}>
      {children}
    </h5>
  )
}

export const AlertDescription = ({ children, className = '', ...props }) => {
  return (
    <div className={`text-sm [&_p]:leading-relaxed ${className}`} {...props}>
      {children}
    </div>
  )
}