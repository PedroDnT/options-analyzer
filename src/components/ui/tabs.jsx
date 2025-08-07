import React, { useState } from 'react'

export const Tabs = ({ children, defaultValue, className = '', ...props }) => {
  const [activeTab, setActiveTab] = useState(defaultValue)
  
  return (
    <div className={`w-full ${className}`} data-active-tab={activeTab} {...props}>
      {React.Children.map(children, child =>
        React.cloneElement(child, { activeTab, setActiveTab })
      )}
    </div>
  )
}

export const TabsList = ({ children, className = '', activeTab, setActiveTab, ...props }) => {
  return (
    <div className={`inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground ${className}`} {...props}>
      {React.Children.map(children, child =>
        React.cloneElement(child, { activeTab, setActiveTab })
      )}
    </div>
  )
}

export const TabsTrigger = ({ children, value, className = '', activeTab, setActiveTab, ...props }) => {
  const isActive = activeTab === value
  
  return (
    <button
      className={`inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ${
        isActive ? 'bg-background text-foreground shadow-sm' : 'hover:bg-muted hover:text-foreground'
      } ${className}`}
      onClick={() => setActiveTab(value)}
      {...props}
    >
      {children}
    </button>
  )
}

export const TabsContent = ({ children, value, className = '', activeTab, ...props }) => {
  if (activeTab !== value) return null
  
  return (
    <div className={`mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${className}`} {...props}>
      {children}
    </div>
  )
}