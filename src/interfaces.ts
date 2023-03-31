import z from 'zod'

export const ZodPromptPostBody = z.object({
  name: z.string().min(1, { message: "Name must be at least 1 character long"}).max(20, { message: "Name must be at most 20 characters long" }),
  filters: z.object({
    schemas: z.string().array().optional().default(["public"]),
    includeTables: z.string().array().optional().default(["*"]),
    excludeTables: z.string().array().optional().default([])
  }).optional().default({
    schemas: ["public"],
    includeTables: ["*"],
    excludeTables: []
  })
})

export type Filters = z.infer<typeof ZodPromptPostBody>['filters']